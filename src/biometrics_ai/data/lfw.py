from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class LfwProtocolConfig:
    identities: int = 60
    samples_per_identity: int = 6
    seed: int = 20260826


def build_lfw_protocol(image_root: str | Path, config: LfwProtocolConfig) -> list[dict[str, str | int]]:
    image_root = Path(image_root)
    if not image_root.is_dir():
        raise FileNotFoundError(f"LFW funneled image root not found: {image_root}")
    if config.identities < 5:
        raise ValueError("At least five identities are required for non-empty train/validation/test splits")
    if config.samples_per_identity < 2:
        raise ValueError("At least two samples per identity are required for gallery/probe evaluation")

    eligible: list[tuple[Path, list[Path]]] = []
    for identity_directory in sorted(path for path in image_root.iterdir() if path.is_dir()):
        images = sorted(identity_directory.glob("*.jpg"))
        if len(images) >= config.samples_per_identity:
            eligible.append((identity_directory, images))
    if len(eligible) < config.identities:
        raise ValueError(f"Requested {config.identities} identities, but only {len(eligible)} are eligible")

    rng = np.random.default_rng(config.seed)
    selected_indices = rng.permutation(len(eligible))[: config.identities]
    train_end = int(0.6 * config.identities)
    validation_end = int(0.8 * config.identities)
    rows: list[dict[str, str | int]] = []
    for protocol_index, eligible_index in enumerate(selected_indices):
        _, images = eligible[int(eligible_index)]
        if protocol_index < train_end:
            split = "train"
        elif protocol_index < validation_end:
            split = "val"
        else:
            split = "test"
        identity_id = f"lfw_{protocol_index:04d}"
        sample_indices = rng.choice(len(images), size=config.samples_per_identity, replace=False)
        for sample_index, image_index in enumerate(sample_indices):
            image_path = images[int(image_index)]
            rows.append(
                {
                    "sample_id": f"{identity_id}_{sample_index:02d}",
                    "identity_id": identity_id,
                    "source_image": image_path.as_posix(),
                    "split": split,
                    "sample_index": sample_index,
                }
            )
    return rows