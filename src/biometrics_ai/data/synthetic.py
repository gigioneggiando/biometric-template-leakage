"""Synthetic, identity-disjoint data used only for engineering validation."""
from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from biometrics_ai.protection import BioHashConfig, biohash, generate_key


@dataclass(frozen=True)
class SyntheticConfig:
    identities: int = 60
    samples_per_identity: int = 12
    embedding_dim: int = 64
    template_dim: int = 32
    seed: int = 7


def identity_splits(identities: int) -> dict[str, np.ndarray]:
    ids = np.arange(identities)
    return {"train": ids[: int(.6 * identities)], "val": ids[int(.6 * identities): int(.8 * identities)], "test": ids[int(.8 * identities):]}


def make_embeddings(config: SyntheticConfig) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(config.seed)
    centers = rng.normal(size=(config.identities, config.embedding_dim))
    centers /= np.linalg.norm(centers, axis=1, keepdims=True)
    values, labels, sample_ids = [], [], []
    for identity in range(config.identities):
        for sample in range(config.samples_per_identity):
            embedding = centers[identity] + 0.08 * rng.normal(size=config.embedding_dim)
            values.append(embedding / np.linalg.norm(embedding))
            labels.append(identity)
            sample_ids.append(f"synthetic_{identity:04d}_{sample:03d}")
    return np.asarray(values, dtype=np.float32), np.asarray(labels), np.asarray(sample_ids)


def build_sets(config: SyntheticConfig, split: str, exposures: int, key_split: str | None = None) -> dict[str, np.ndarray]:
    if not 1 <= exposures <= config.samples_per_identity:
        raise ValueError("exposures must be between 1 and samples_per_identity")
    embeddings, labels, _ = make_embeddings(config)
    selected_ids = identity_splits(config.identities)[split]
    key_scope = key_split or split
    scheme = BioHashConfig(input_dim=config.embedding_dim, output_dim=config.template_dim)
    templates, targets, set_labels, key_ids = [], [], [], []
    for identity in selected_ids:
        indices = np.flatnonzero(labels == identity)[:exposures]
        per_set, per_keys = [], []
        for exposure, index in enumerate(indices):
            key = generate_key(config.seed, key_scope, identity * 1000 + exposure)
            per_set.append(biohash(embeddings[index], key, scheme))
            per_keys.append(key)
        templates.append(per_set)
        target = embeddings[indices].mean(axis=0)
        targets.append(target / np.linalg.norm(target))
        set_labels.append(identity)
        key_ids.append(per_keys)
    return {"templates": np.asarray(templates, dtype=np.float32), "targets": np.asarray(targets, dtype=np.float32),
            "identity_ids": np.asarray(set_labels), "key_ids": np.asarray(key_ids, dtype=np.uint64)}
