from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class MobioProtocolConfig:
    identities: int = 150
    samples_per_identity: int = 12
    seed: int = 20260904


def _session_id(image: Path) -> str:
    parts = image.stem.split("_")
    if len(parts) < 3:
        raise ValueError(f"Unexpected MOBIO filename: {image.name}")
    return parts[1]


def build_mobio_protocol(image_root: str | Path, config: MobioProtocolConfig) -> list[dict[str, str | int]]:
    image_root = Path(image_root)
    if not image_root.is_dir():
        raise FileNotFoundError(f"MOBIO selected-image root not found: {image_root}")
    if config.identities < 5:
        raise ValueError("At least five identities are required for non-empty train/validation/test splits")
    if config.samples_per_identity < 2:
        raise ValueError("At least two samples per identity are required")

    eligible: list[tuple[str, dict[str, list[Path]]]] = []
    for identity_directory in sorted(path for path in image_root.iterdir() if path.is_dir()):
        sessions: dict[str, list[Path]] = {}
        for image in sorted(identity_directory.glob("*.jpg")):
            sessions.setdefault(_session_id(image), []).append(image)
        if len(sessions) >= config.samples_per_identity:
            eligible.append((identity_directory.name, sessions))
    if len(eligible) < config.identities:
        raise ValueError(f"Requested {config.identities} identities, but only {len(eligible)} are eligible")

    rng = np.random.default_rng(config.seed)
    selected_indices = rng.permutation(len(eligible))[: config.identities]
    train_end = int(0.6 * config.identities)
    validation_end = int(0.8 * config.identities)
    rows: list[dict[str, str | int]] = []
    for protocol_index, eligible_index in enumerate(selected_indices):
        identity_id, sessions = eligible[int(eligible_index)]
        if protocol_index < train_end:
            split = "train"
        elif protocol_index < validation_end:
            split = "val"
        else:
            split = "test"
        selected_sessions = rng.choice(sorted(sessions), size=config.samples_per_identity, replace=False)
        for sample_index, session_id in enumerate(selected_sessions):
            images = sessions[str(session_id)]
            image = images[int(rng.integers(len(images)))]
            rows.append(
                {
                    "sample_id": image.stem,
                    "identity_id": identity_id,
                    "source_image": image.as_posix(),
                    "split": split,
                    "sample_index": sample_index,
                    "session_id": str(session_id),
                }
            )
    return rows