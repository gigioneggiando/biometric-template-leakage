"""Paper-specified MLP-Hash reference implementation.

The public paper specifies ReLU, three hidden layers of width twice the input,
and output-mean binarization. Its row-orthonormal wording is impossible for the
narrowing output layer, so this implementation uses the standard
semi-orthogonal extension and is not labelled source-exact.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .biohash import _seed_from_key


@dataclass(frozen=True)
class MLPHashConfig:
    input_dim: int = 512
    output_dim: int = 512
    hidden_dim: int = 1024
    hidden_layers: int = 3


def _semi_orthogonal_projection(input_dim: int, output_dim: int, rng: np.random.Generator) -> np.ndarray:
    if output_dim >= input_dim:
        matrix = rng.standard_normal((output_dim, input_dim), dtype=np.float64)
        projection, _ = np.linalg.qr(matrix, mode="reduced")
        return projection.T.astype(np.float32)
    matrix = rng.standard_normal((input_dim, output_dim), dtype=np.float64)
    projection, _ = np.linalg.qr(matrix, mode="reduced")
    return projection.astype(np.float32)


def _validate_config(config: MLPHashConfig) -> None:
    if min(config.input_dim, config.output_dim, config.hidden_dim, config.hidden_layers) <= 0:
        raise ValueError("MLP-Hash dimensions and hidden_layers must be positive")


def mlphash(
    embedding: np.ndarray,
    key: int | str | bytes,
    config: MLPHashConfig = MLPHashConfig(),
) -> np.ndarray:
    _validate_config(config)
    values = np.asarray(embedding, dtype=np.float32)
    if values.shape != (config.input_dim,):
        raise ValueError(f"Expected embedding shape {(config.input_dim,)}, got {values.shape}")

    rng = np.random.default_rng(_seed_from_key(key))
    layer_dims = [config.input_dim] + [config.hidden_dim] * config.hidden_layers + [config.output_dim]
    for input_dim, output_dim in zip(layer_dims, layer_dims[1:]):
        values = np.maximum(values @ _semi_orthogonal_projection(input_dim, output_dim, rng), 0.0)
    return (values > values.mean()).astype(np.uint8)


def mlphash_batch(
    embeddings: np.ndarray,
    key: int | str | bytes,
    config: MLPHashConfig = MLPHashConfig(),
) -> np.ndarray:
    _validate_config(config)
    values = np.asarray(embeddings, dtype=np.float32)
    if values.ndim != 2 or values.shape[1] != config.input_dim:
        raise ValueError(f"Expected embedding shape (n, {config.input_dim}), got {values.shape}")

    rng = np.random.default_rng(_seed_from_key(key))
    layer_dims = [config.input_dim] + [config.hidden_dim] * config.hidden_layers + [config.output_dim]
    for input_dim, output_dim in zip(layer_dims, layer_dims[1:]):
        values = np.maximum(values @ _semi_orthogonal_projection(input_dim, output_dim, rng), 0.0)
    thresholds = values.mean(axis=1, keepdims=True)
    return (values > thresholds).astype(np.uint8)