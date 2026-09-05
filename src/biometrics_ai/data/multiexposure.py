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


def shuffle_non_anchor_records(exposure_set: dict[str, np.ndarray], seed: int) -> dict[str, np.ndarray]:
    """Replace every record after the first with a record from another identity.

    The operation preserves the number of records, the per-position marginal
    distribution, and one correctly assigned anchor record in every set.
    """
    templates = np.asarray(exposure_set["templates"])
    if templates.ndim != 3:
        raise ValueError("Exposure templates must have shape [sets, exposures, features]")
    if templates.shape[1] <= 1:
        return {**exposure_set, "templates": templates.copy()}

    identity_ids = np.asarray(exposure_set["identity_ids"])
    identities = np.unique(identity_ids)
    if len(identities) < 2:
        raise ValueError("Shuffling requires at least two identities")
    grouped = {identity: np.flatnonzero(identity_ids == identity) for identity in identities}
    group_sizes = {len(indices) for indices in grouped.values()}
    if len(group_sizes) != 1:
        raise ValueError("Shuffling requires the same number of sets per identity")

    shuffled = templates.copy()
    rng = np.random.default_rng(seed)
    for position in range(1, templates.shape[1]):
        identity_order = rng.permutation(identities)
        shift = int(rng.integers(1, len(identities)))
        for index, target_identity in enumerate(identity_order):
            donor_identity = identity_order[(index + shift) % len(identities)]
            target_rows = grouped[target_identity]
            donor_rows = rng.permutation(grouped[donor_identity])
            shuffled[target_rows, position] = templates[donor_rows, position]

    return {**exposure_set, "templates": shuffled}
