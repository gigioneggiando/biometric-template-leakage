"""Deterministic identity-disjoint protocol for the FEI face database.

FEI images are named ``<subject>-<pose>.jpg`` with subjects 1..200 and poses
01..14 (11 profile-rotation steps, two frontal expressions, one illumination
variant). The protocol keeps all identities with at least ``samples_per_identity``
images, selects images per identity with a seeded permutation, and assigns
identities to 60/20/20 train/validation/test splits.
"""
from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

import numpy as np

_NAME = re.compile(r"^(?P<subject>\d+)-(?P<pose>\d+)\.jpe?g$", re.IGNORECASE)


@dataclass(frozen=True)
class FeiProtocolConfig:
    identities: int = 200
    samples_per_identity: int = 12
    seed: int = 20260912


def build_fei_protocol(image_root: str | Path, config: FeiProtocolConfig) -> list[dict[str, str | int]]:
    image_root = Path(image_root)
    if not image_root.is_dir():
        raise FileNotFoundError(f"FEI image root not found: {image_root}")
    if config.identities < 5:
        raise ValueError("At least five identities are required for non-empty splits")
    if config.samples_per_identity < 2:
        raise ValueError("At least two samples per identity are required")

    grouped: dict[int, list[tuple[int, Path]]] = defaultdict(list)
    for path in image_root.rglob("*"):
        match = _NAME.match(path.name)
        if match:
            grouped[int(match["subject"])].append((int(match["pose"]), path))
    eligible = sorted(subject for subject, images in grouped.items() if len(images) >= config.samples_per_identity)
    if len(eligible) < config.identities:
        raise ValueError(f"Requested {config.identities} identities, but only {len(eligible)} have enough images")

    rng = np.random.default_rng(config.seed)
    selected = [eligible[int(index)] for index in rng.permutation(len(eligible))[: config.identities]]
    train_end = int(0.6 * config.identities)
    validation_end = int(0.8 * config.identities)
    rows: list[dict[str, str | int]] = []
    for protocol_index, subject in enumerate(selected):
        split = "train" if protocol_index < train_end else "val" if protocol_index < validation_end else "test"
        images = sorted(grouped[subject])
        chosen = rng.choice(len(images), size=config.samples_per_identity, replace=False)
        identity_id = f"fei_{subject:03d}"
        for sample_index, image_index in enumerate(sorted(int(i) for i in chosen)):
            pose, path = images[image_index]
            rows.append(
                {
                    "sample_id": f"{identity_id}_{sample_index:02d}",
                    "identity_id": identity_id,
                    "source_image": path.as_posix(),
                    "split": split,
                    "sample_index": sample_index,
                    "pose_id": pose,
                }
            )
    return rows
