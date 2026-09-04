from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

import numpy as np

from biometrics_ai.protection import generate_key


@dataclass(frozen=True)
class ExposureSetConfig:
    exposures: int
    repeats_per_identity: int = 8
    seed: int = 20260904


def build_real_exposure_sets(
    embeddings: np.ndarray,
    templates: np.ndarray,
    metadata: list[dict],
    split: str,
    config: ExposureSetConfig,
) -> dict[str, np.ndarray]:
    if not 1 <= config.exposures <= 10:
        raise ValueError("exposures must be between 1 and 10")
    if config.repeats_per_identity < 1:
        raise ValueError("repeats_per_identity must be positive")
    if len(embeddings) != len(templates) or len(embeddings) != len(metadata):
        raise ValueError("Embeddings, templates, and metadata must have equal lengths")

    grouped: dict[str, list[int]] = defaultdict(list)
    for index, row in enumerate(metadata):
        if row["split"] == split:
            grouped[str(row["identity_id"])].append(index)
    if not grouped:
        raise ValueError(f"No identities found for split {split!r}")

    set_templates, targets, identity_ids, set_ids = [], [], [], []
    gallery_embeddings, gallery_identity_ids = [], []
    for identity_id in sorted(grouped):
        indices = sorted(grouped[identity_id], key=lambda index: int(metadata[index]["sample_index"]))
        gallery_index, exposure_indices = indices[0], np.asarray(indices[1:])
        if len(exposure_indices) < 10:
            raise ValueError(f"Identity {identity_id} has only {len(exposure_indices)} exposure candidates")
        gallery_embeddings.append(embeddings[gallery_index])
        gallery_identity_ids.append(identity_id)
        for repeat in range(config.repeats_per_identity):
            plan_seed = generate_key(config.seed, split, f"{identity_id}:{repeat}")
            ordered_indices = np.random.default_rng(plan_seed).permutation(exposure_indices)
            selected = ordered_indices[: config.exposures]
            target = embeddings[selected].mean(axis=0)
            target /= np.linalg.norm(target).clip(min=1e-12)
            set_templates.append(templates[selected])
            targets.append(target)
            identity_ids.append(identity_id)
            set_ids.append(f"{split}:{identity_id}:{repeat}")

    return {
        "templates": np.asarray(set_templates, dtype=np.float32),
        "targets": np.asarray(targets, dtype=np.float32),
        "identity_ids": np.asarray(identity_ids),
        "set_ids": np.asarray(set_ids),
        "gallery": np.asarray(gallery_embeddings, dtype=np.float32),
        "gallery_identity_ids": np.asarray(gallery_identity_ids),
    }