"""Download and verify the public CFP research dataset from its official site."""
from __future__ import annotations

import argparse
import hashlib
import json
import urllib.request
import zipfile
from pathlib import Path


# The official host has no trusted HTTPS endpoint; verify this pinned digest before extraction.
ARCHIVE_URL = "http://www.cfpw.io/cfp-dataset.zip"
ARCHIVE_SHA256 = "666b87635e6af028177ac72a85f03099fac263baf09c21f333fa445f930f65b1"


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
    parser.add_argument("--root", type=Path, default=Path("data/raw/cfp"))
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()

    archive = args.root / "cfp-dataset.zip"
    dataset_root = args.root / "cfp-dataset"
    if not archive.exists():
        if args.verify_only:
            raise SystemExit(f"CFP archive not found: {archive}")
        args.root.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(ARCHIVE_URL, archive)
    archive_hash = digest(archive)
    if archive_hash != ARCHIVE_SHA256:
        raise SystemExit(f"Unexpected CFP archive SHA-256: {archive_hash}")
    if not args.verify_only and not dataset_root.exists():
        extract_safely(archive, args.root)

    image_root = dataset_root / "Data" / "Images"
    identity_directories = sorted(path for path in image_root.iterdir() if path.is_dir())
    frontal_count = sum(len(list((path / "frontal").glob("*.jpg"))) for path in identity_directories)
    profile_count = sum(len(list((path / "profile").glob("*.jpg"))) for path in identity_directories)
    if (len(identity_directories), frontal_count, profile_count) != (500, 5000, 2000):
        raise SystemExit(
            "Unexpected CFP contents: "
            f"identities={len(identity_directories)}, frontal={frontal_count}, profile={profile_count}"
        )
    print(
        json.dumps(
            {
                "name": "Celebrities in Frontal-Profile",
                "source": ARCHIVE_URL,
                "access": "official hash-pinned HTTP research download; archive contains no explicit license file",
                "archive_sha256": archive_hash,
                "identities": len(identity_directories),
                "frontal_images": frontal_count,
                "profile_images": profile_count,
                "image_root": image_root.as_posix(),
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()