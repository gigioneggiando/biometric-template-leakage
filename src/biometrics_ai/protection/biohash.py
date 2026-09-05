"""Deterministic BioHashing reference implementation for controlled experiments.

This implementation is for the proposed experiment and must not be labelled an
exact implementation of benchmark_cb until its upstream source is recovered and
the parameterization is cross-checked.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib

import numpy as np


@dataclass(frozen=True)
class BioHashConfig:
    input_dim: int = 512
    output_dim: int = 128
    threshold: float = 0.0
    # Multiply Q by sign(diag R) so the projection is exactly Haar (Mezzadri 2007).
    haar_sign_corrected: bool = False


def _seed_from_key(key: int | str | bytes) -> int:
    raw = str(key).encode("utf-8") if not isinstance(key, bytes) else key
    return int.from_bytes(hashlib.sha256(raw).digest()[:8], "little", signed=False)


def generate_key(master_seed: int, split: str, index: int | str) -> int:
    """Generate a stable split-scoped key identifier without hidden global state."""
    return _seed_from_key(f"biohash:{master_seed}:{split}:{index}")


def _orthonormal_projection(
    input_dim: int, output_dim: int, key: int | str | bytes, haar_sign_corrected: bool = False
) -> np.ndarray:
    if output_dim > input_dim:
        raise ValueError("BioHash output_dim must not exceed input_dim")
    rng = np.random.default_rng(_seed_from_key(key))
    matrix = rng.standard_normal((input_dim, output_dim), dtype=np.float64)
    q, r = np.linalg.qr(matrix, mode="reduced")
    if haar_sign_corrected:
        q = q * np.sign(np.diag(r))
    return q[:, :output_dim].astype(np.float32)


def biohash(embedding: np.ndarray, key: int | str | bytes, config: BioHashConfig = BioHashConfig()) -> np.ndarray:
    embedding = np.asarray(embedding, dtype=np.float32)
    if embedding.shape != (config.input_dim,):
        raise ValueError(f"Expected embedding shape {(config.input_dim,)}, got {embedding.shape}")
    projection = _orthonormal_projection(config.input_dim, config.output_dim, key, config.haar_sign_corrected)
    return (embedding @ projection >= config.threshold).astype(np.uint8)


def biohash_batch(embeddings: np.ndarray, key: int | str | bytes, config: BioHashConfig = BioHashConfig()) -> np.ndarray:
    embeddings = np.asarray(embeddings, dtype=np.float32)
    if embeddings.ndim != 2 or embeddings.shape[1] != config.input_dim:
        raise ValueError(f"Expected embedding shape (n, {config.input_dim}), got {embeddings.shape}")
    projection = _orthonormal_projection(config.input_dim, config.output_dim, key, config.haar_sign_corrected)
    return (embeddings @ projection >= config.threshold).astype(np.uint8)


def _correlated_orthonormal_projection(
    input_dim: int,
    output_dim: int,
    shared_key: int | str | bytes,
    private_key: int | str | bytes,
    shared_dimensions: int,
    haar_sign_corrected: bool = True,
) -> np.ndarray:
    """Build an orthonormal projection with an exact shared column prefix."""
    if not 0 <= shared_dimensions <= output_dim:
        raise ValueError("shared_dimensions must be between zero and output_dim")
    shared_projection = _orthonormal_projection(input_dim, output_dim, shared_key, haar_sign_corrected)
    if shared_dimensions == output_dim:
        return shared_projection

    shared_basis = shared_projection[:, :shared_dimensions]
    private_dimensions = output_dim - shared_dimensions
    rng = np.random.default_rng(_seed_from_key(private_key))
    candidates = rng.standard_normal((input_dim, private_dimensions), dtype=np.float64)
    if shared_dimensions:
        candidates -= shared_basis @ (shared_basis.T @ candidates)
    private_basis, private_r = np.linalg.qr(candidates, mode="reduced")
    if haar_sign_corrected:
        private_basis = private_basis * np.sign(np.diag(private_r))
    return np.concatenate(
        [shared_basis, private_basis[:, :private_dimensions].astype(np.float32)], axis=1
    )


def correlated_biohash(
    embedding: np.ndarray,
    shared_key: int | str | bytes,
    private_key: int | str | bytes,
    shared_dimensions: int,
    config: BioHashConfig = BioHashConfig(),
) -> np.ndarray:
    """BioHash with controlled partial projection reuse across record keys."""
    embedding = np.asarray(embedding, dtype=np.float32)
    if embedding.shape != (config.input_dim,):
        raise ValueError(f"Expected embedding shape {(config.input_dim,)}, got {embedding.shape}")
    projection = _correlated_orthonormal_projection(
        config.input_dim,
        config.output_dim,
        shared_key,
        private_key,
        shared_dimensions,
        config.haar_sign_corrected,
    )
    return (embedding @ projection >= config.threshold).astype(np.uint8)
