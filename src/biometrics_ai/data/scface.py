"""Deterministic identity-disjoint protocol for the SCface database."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np


@dataclass(frozen=True)
class ScfaceProtocolConfig:
    identities: int = 130
    seed: int = 20260918


def build_scface_protocol(
    image_root: str | Path,
    config: ScfaceProtocolConfig = ScfaceProtocolConfig(),
) -> list[dict[str, str | int]]:
    """Use one visible mugshot as gallery and 21 visible surveillance probes."""
    image_root = Path(image_root)
    frontal_root = image_root / "mugshot_frontal_cropped_all"
    surveillance_root = image_root / "surveillance_cameras_all"
    if not frontal_root.is_dir() or not surveillance_root.is_dir():
        raise FileNotFoundError("SCface mugshot and surveillance directories are required")
    if config.identities < 5 or config.identities > 130:
        raise ValueError("SCface identities must be between 5 and 130")

    eligible: list[tuple[int, Path, list[tuple[int, int, Path]]]] = []
    for subject in range(1, 131):
        frontal = frontal_root / f"{subject:03d}_frontal.JPG"
        if not frontal.is_file():
            frontal = frontal_root / f"{subject:03d}_frontal.jpg"
        surveillance = [
            (camera, distance, surveillance_root / f"{subject:03d}_cam{camera}_{distance}.jpg")
            for distance in range(1, 4)
            for camera in range(1, 8)
        ]
        if frontal.is_file() and all(path.is_file() for _, _, path in surveillance):
            eligible.append((subject, frontal, surveillance))
    if len(eligible) < config.identities:
        raise ValueError(
            f"Requested {config.identities} identities, but only {len(eligible)} have the complete visible protocol"
        )

    rng = np.random.default_rng(config.seed)
    selected = [eligible[int(index)] for index in rng.permutation(len(eligible))[: config.identities]]
    train_end = int(0.6 * config.identities)
    validation_end = int(0.8 * config.identities)
    rows: list[dict[str, str | int]] = []
    for protocol_index, (subject, frontal, surveillance) in enumerate(selected):
        split = "train" if protocol_index < train_end else "val" if protocol_index < validation_end else "test"
        identity_id = f"scface_{subject:03d}"
        rows.append(
            {
                "sample_id": f"{identity_id}_gallery",
                "identity_id": identity_id,
                "source_image": frontal.as_posix(),
                "split": split,
                "sample_index": 0,
                "capture_type": "visible_mugshot_gallery",
                "camera_id": 0,
                "distance_id": 0,
            }
        )
        for sample_index, (camera, distance, path) in enumerate(surveillance, start=1):
            rows.append(
                {
                    "sample_id": f"{identity_id}_cam{camera}_d{distance}",
                    "identity_id": identity_id,
                    "source_image": path.as_posix(),
                    "split": split,
                    "sample_index": sample_index,
                    "capture_type": "visible_surveillance_exposure",
                    "camera_id": camera,
                    "distance_id": distance,
                }
            )
    return rows
