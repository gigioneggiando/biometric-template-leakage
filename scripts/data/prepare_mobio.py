"""Prepare metadata only after the researcher has obtained MOBIO lawfully."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(block)
    return hasher.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate a user-provided, authorized MOBIO root.")
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/manifest.json"))
    args = parser.parse_args()
    if not args.root.is_dir():
        raise SystemExit("MOBIO root not found. Obtain the dataset through Idiap and pass its authorized local path.")
    files = [p for p in args.root.rglob("*") if p.is_file()]
    payload = {"name": "MOBIO", "source": "https://www.idiap.ch/en/scientific-research/data/mobio", "access": "manual registration/license required", "local_root": str(args.root), "file_count": len(files),
               "sample_checksums": {str(p.relative_to(args.root)): digest(p) for p in files[:100]}, "status": "prepared; protocol mapping requires the exact upstream benchmark configuration"}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Wrote {args.output} for {len(files)} files")


if __name__ == "__main__":
    main()
