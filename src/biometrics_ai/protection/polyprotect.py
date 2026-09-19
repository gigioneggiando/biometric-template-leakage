"""Paper-specified PolyProtect with explicit coefficient and exponent policies."""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations

import numpy as np

from .biohash import _seed_from_key


@dataclass(frozen=True)
class PolyProtectConfig:
    input_dim: int = 512
    window_size: int = 5
    overlap: int = 2
    coefficient_bound: int = 50

    def __post_init__(self):
        if self.window_size < 1 or self.input_dim < self.window_size:
            raise ValueError("PolyProtect requires input_dim >= window_size >= 1")
        if not 0 <= self.overlap < self.window_size:
            raise ValueError("PolyProtect overlap must be smaller than the window")
        if self.coefficient_bound < 1 or 2 * self.coefficient_bound < self.window_size:
            raise ValueError("Coefficient range cannot supply distinct nonzero coefficients")

    @property
    def output_dim(self) -> int:
        stride = self.window_size - self.overlap
        return (self.input_dim - self.window_size + stride - 1) // stride + 1


def polyprotect_parameters(key: int | str | bytes, config: PolyProtectConfig) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(_seed_from_key(key))
    candidates = np.concatenate((np.arange(-config.coefficient_bound, 0), np.arange(1, config.coefficient_bound + 1)))
    return rng.choice(candidates, config.window_size, replace=False), rng.permutation(np.arange(1, config.window_size + 1))


def polyprotect_parameters_stricter(
    key: int | str | bytes,
    development_embeddings: np.ndarray,
    development_identity_ids,
    config: PolyProtectConfig = PolyProtectConfig(),
    candidates: int = 50,
    unlinkable_band: float = 0.5,
    max_development_pairs: int | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Score-conditioned parameter selection approximating PolyProtect paper Section IV-D.

    The paper reports that naive random (C, E) selection leaves mated (genuine-pair)
    comparison scores with extreme bumps near +-1, and proposes selecting parameters so
    mated scores instead concentrate within a "full unlinkability" range. The paper does
    not give a closed-form selection objective, so this is our own concrete
    operationalization, not a source-exact reproduction: among `candidates` parameter
    sets drawn the same way as `polyprotect_parameters`, keep the one minimizing the mean
    amount by which mated cosine scores on `development_embeddings` fall outside
    [-unlinkable_band, unlinkable_band]. Selection uses only the development set; it must
    not be the evaluation/attack data. `max_development_pairs` deterministically subsamples
    mated pairs (seeded by `key`) when there are more than that many, trading selection
    precision for runtime on large development sets; `None` uses every mated pair.
    """
    values = np.asarray(development_embeddings, dtype=np.float64)
    identities = np.asarray(development_identity_ids)
    if values.ndim != 2 or values.shape[-1] != config.input_dim:
        raise ValueError("Development set must be a matrix of input_dim-length embeddings")
    if len(identities) != len(values):
        raise ValueError("development_identity_ids must have one entry per development row")
    mated = [pair for identity in np.unique(identities) for pair in combinations(np.flatnonzero(identities == identity), 2)]
    if not mated:
        raise ValueError("Development set needs at least one identity with two records")
    if max_development_pairs is not None and len(mated) > max_development_pairs:
        if max_development_pairs < 1:
            raise ValueError("max_development_pairs must be positive when given")
        rng = np.random.default_rng(_seed_from_key(f"{key}:stricter_pair_subsample"))
        mated = [mated[index] for index in rng.choice(len(mated), max_development_pairs, replace=False)]
    left = values[[pair[0] for pair in mated]]
    right = values[[pair[1] for pair in mated]]
    best_extremeness, best_parameters = np.inf, None
    for index in range(candidates):
        coefficients, exponents = polyprotect_parameters(f"{key}:stricter_candidate:{index}", config)
        protected_left = polyprotect_with_parameters(left, coefficients, exponents, config)
        protected_right = polyprotect_with_parameters(right, coefficients, exponents, config)
        mated_scores = np.sum(protected_left * protected_right, axis=-1) / (
            np.linalg.norm(protected_left, axis=-1) * np.linalg.norm(protected_right, axis=-1) + 1e-12
        )
        extremeness = float(np.mean(np.maximum(0.0, np.abs(mated_scores) - unlinkable_band)))
        if extremeness < best_extremeness:
            best_extremeness, best_parameters = extremeness, (coefficients, exponents)
    return best_parameters


def polyprotect_with_parameters(embeddings: np.ndarray, coefficients: np.ndarray,
                                exponents: np.ndarray, config: PolyProtectConfig) -> np.ndarray:
    values = np.asarray(embeddings, dtype=np.float64)
    coefficients, exponents = np.asarray(coefficients), np.asarray(exponents)
    if values.ndim not in (1, 2) or values.shape[-1] != config.input_dim or not np.isfinite(values).all():
        raise ValueError("PolyProtect expects finite input_dim vectors")
    if (coefficients.shape != (config.window_size,) or not np.isfinite(coefficients).all()
            or not np.equal(coefficients, np.floor(coefficients)).all()
            or np.unique(coefficients).size != config.window_size or (coefficients == 0).any()
            or (np.abs(coefficients) > config.coefficient_bound).any()):
        raise ValueError("Invalid unique nonzero integer coefficients")
    if exponents.shape != (config.window_size,) or not np.array_equal(np.sort(exponents), np.arange(1, config.window_size + 1)):
        raise ValueError("Exponents must be a permutation of 1..window_size")
    stride = config.window_size - config.overlap
    padded_dim = (config.output_dim - 1) * stride + config.window_size
    padding = [(0, 0)] * values.ndim
    padding[-1] = (0, padded_dim - config.input_dim)
    windows = np.lib.stride_tricks.sliding_window_view(np.pad(values, padding), config.window_size, axis=-1)[..., ::stride, :]
    with np.errstate(over="raise", invalid="raise"):
        protected = np.sum(coefficients * windows ** exponents, axis=-1).astype(np.float32)
    if not np.isfinite(protected).all():
        raise ValueError("PolyProtect produced nonfinite values")
    return protected


def polyprotect_batch(embeddings: np.ndarray, key: int | str | bytes,
                      config: PolyProtectConfig = PolyProtectConfig()) -> np.ndarray:
    values = np.asarray(embeddings)
    if values.ndim != 2:
        raise ValueError("PolyProtect batch expects a matrix")
    return polyprotect_with_parameters(values, *polyprotect_parameters(key, config), config)


def polyprotect(embedding: np.ndarray, key: int | str | bytes,
                config: PolyProtectConfig = PolyProtectConfig()) -> np.ndarray:
    values = np.asarray(embedding)
    if values.shape != (config.input_dim,):
        raise ValueError("PolyProtect expects one input_dim vector")
    return polyprotect_with_parameters(values, *polyprotect_parameters(key, config), config)