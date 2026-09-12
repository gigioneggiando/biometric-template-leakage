"""Paper-specified Gaussian index-of-maximum hashing, not source-exact."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .biohash import _seed_from_key


@dataclass(frozen=True)
class IoMGRPConfig:
    input_dim: int = 512
    groups: int = 300
    group_size: int = 16

    def __post_init__(self):
        if min(self.input_dim, self.groups) < 1 or self.group_size < 2:
            raise ValueError("IoM-GRP requires positive dimensions and at least two categories")


def _projection_matrix(key: int | str | bytes, config: IoMGRPConfig) -> np.ndarray:
    rng = np.random.default_rng(_seed_from_key(key))
    return rng.standard_normal((config.input_dim, config.groups * config.group_size)).astype(np.float32)


def iomgrp_batch(embeddings: np.ndarray, key: int | str | bytes,
                 config: IoMGRPConfig = IoMGRPConfig()) -> np.ndarray:
    values = np.asarray(embeddings, dtype=np.float32)
    if values.ndim != 2 or values.shape[1] != config.input_dim or not np.isfinite(values).all():
        raise ValueError("IoM-GRP expects finite rows of input_dim values")
    projections = values @ _projection_matrix(key, config)
    return projections.reshape(len(values), config.groups, config.group_size).argmax(axis=-1).astype(np.int32)


def iomgrp(embedding: np.ndarray, key: int | str | bytes,
           config: IoMGRPConfig = IoMGRPConfig()) -> np.ndarray:
    values = np.asarray(embedding)
    if values.shape != (config.input_dim,):
        raise ValueError("IoM-GRP expects one input_dim vector")
    return iomgrp_batch(values[None, :], key, config)[0]


def iomgrp_encoded_batch(embeddings: np.ndarray, key: int | str | bytes,
                         config: IoMGRPConfig = IoMGRPConfig()) -> np.ndarray:
    indices = iomgrp_batch(embeddings, key, config)
    return np.eye(config.group_size, dtype=np.uint8)[indices].reshape(len(indices), config.groups * config.group_size)


def iomgrp_encoded(embedding: np.ndarray, key: int | str | bytes,
                   config: IoMGRPConfig = IoMGRPConfig()) -> np.ndarray:
    indices = iomgrp(embedding, key, config)
    return np.eye(config.group_size, dtype=np.uint8)[indices].reshape(-1)