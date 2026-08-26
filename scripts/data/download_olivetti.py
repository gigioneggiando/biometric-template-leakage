"""Fetch and materialize the real AT&T Olivetti faces dataset."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image
from sklearn.datasets import fetch_olivetti_faces


CACHE_SHA256 = "47398b319d88c78459514b30b87c562313aad345b5c6a387b678d7f8177be4ba"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-home", type=Path, default=Path("data/raw/olivetti"))
    parser.add_argument("--output", type=Path, default=Path("data/raw/olivetti/images"))
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    dataset = fetch_olivetti_faces(
        data_home=str(args.data_home),
        shuffle=False,
        download_if_missing=not args.verify_only,
    )
    cache_path = args.data_home / "olivetti_py3.pkz"
    cache_hash = digest(cache_path)
    if cache_hash != CACHE_SHA256:
        raise SystemExit(f"Unexpected Olivetti cache SHA-256: {cache_hash}")
    if not args.verify_only:
        for identity in range(40):
            identity_directory = args.output / f"{identity:02d}"
            identity_directory.mkdir(parents=True, exist_ok=True)
            indices = np.flatnonzero(dataset.target == identity)
            for sample_index, dataset_index in enumerate(indices):
                pixels = np.clip(dataset.images[int(dataset_index)] * 255, 0, 255).astype(np.uint8)
                Image.fromarray(pixels, mode="L").save(identity_directory / f"{sample_index:02d}.png")

    image_count = len(list(args.output.glob("*/*.png"))) if args.output.exists() else 0
    if not args.verify_only and image_count != 400:
        raise SystemExit(f"Expected 400 materialized Olivetti images, found {image_count}")
    print(
        json.dumps(
            {
                "name": "Olivetti faces",
                "source": "AT&T Laboratories Cambridge via sklearn.datasets.fetch_olivetti_faces",
                "access": "public research dataset; attribution requested by the source",
                "cache_sha256": cache_hash,
                "identities": 40,
                "images": 400,
                "dimensions": [64, 64],
                "image_root": args.output.as_posix(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()