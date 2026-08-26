"""Download and verify InsightFace buffalo_l for non-commercial research use."""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path


ARCHIVE_URL = "https://github.com/deepinsight/insightface/releases/download/v0.7/buffalo_l.zip"
ARCHIVE_SHA256 = "80ffe37d8a5940d59a7384c201a2a38d4741f2f3c51eef46ebb28218a7b0ca2f"
MODEL_HASHES = {
    "det_10g.onnx": "5838f7fe053675b1c7a08b633df49e7af5495cee0493c7dcf6697200b85b5b91",
    "w600k_r50.onnx": "4c06341c33c2ca1f86781dab0e829f88ad5b64be9fba56e56bc9ebdefc619e43",
}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def extract_safely(archive: Path, output: Path) -> None:
    output_root = output.resolve()
    with zipfile.ZipFile(archive) as bundle:
        for member in bundle.infolist():
            destination = (output / member.filename).resolve()
            if output_root not in destination.parents and destination != output_root:
                raise ValueError(f"Unsafe archive member: {member.filename}")
        bundle.extractall(output)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archive", type=Path, default=Path("models/insightface/buffalo_l.zip"))
    parser.add_argument("--output", type=Path, default=Path("models/insightface/buffalo_l"))
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--accept-research-only-license", action="store_true")
    args = parser.parse_args()

    if not args.verify_only and not args.accept_research_only_license:
        raise SystemExit("InsightFace-provided weights are for non-commercial research only; pass --accept-research-only-license after reviewing the upstream terms.")
    if not args.archive.exists():
        if args.verify_only:
            raise SystemExit(f"Archive not found: {args.archive}")
        args.archive.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(ARCHIVE_URL) as response, args.archive.open("wb") as handle:
            while block := response.read(1 << 20):
                handle.write(block)
    archive_hash = digest(args.archive)
    if archive_hash != ARCHIVE_SHA256:
        raise SystemExit(f"Unexpected archive SHA-256: {archive_hash}")

    if not args.verify_only:
        args.output.mkdir(parents=True, exist_ok=True)
        extract_safely(args.archive, args.output)
    model_hashes = {}
    for filename, expected_hash in MODEL_HASHES.items():
        model_path = args.output / filename
        if not model_path.is_file():
            raise SystemExit(f"Expected model not found: {model_path}")
        model_hash = digest(model_path)
        if model_hash != expected_hash:
            raise SystemExit(f"Unexpected SHA-256 for {filename}: {model_hash}")
        model_hashes[filename] = model_hash
    print(json.dumps({"source": ARCHIVE_URL, "archive_sha256": archive_hash, "model_sha256": model_hashes}, indent=2))


if __name__ == "__main__":
    main()