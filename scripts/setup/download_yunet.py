"""Download and verify the Apache-2.0 OpenCV Zoo YuNet detector."""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
from pathlib import Path


MODEL_URL = "https://github.com/opencv/opencv_zoo/raw/main/models/face_detection_yunet/face_detection_yunet_2023mar.onnx"
MODEL_SHA256 = "8f2383e4dd3cfbb4553ea8718107fc0423210dc964f9f4280604804ed2552fa4"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("models/opencv_zoo/face_detection_yunet_2023mar.onnx"),
    )
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    if not args.output.exists():
        if args.verify_only:
            raise SystemExit(f"YuNet model not found: {args.output}")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(MODEL_URL, args.output)
    model_hash = digest(args.output)
    if model_hash != MODEL_SHA256:
        raise SystemExit(f"Unexpected YuNet SHA-256: {model_hash}")
    print(
        json.dumps(
            {
                "source": MODEL_URL,
                "license": "Apache-2.0 (OpenCV Zoo)",
                "model_sha256": model_hash,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()