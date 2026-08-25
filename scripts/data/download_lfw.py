"""Download LFW only through sklearn's documented UMass source."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from sklearn.datasets import fetch_lfw_people


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-home", type=Path, default=Path("data/raw/lfw"))
    parser.add_argument("--min-faces-per-person", type=int, default=2)
    args = parser.parse_args()
    dataset = fetch_lfw_people(data_home=str(args.data_home), min_faces_per_person=args.min_faces_per_person, resize=1.0, color=True, download_if_missing=True)
    manifest = {"name": "LFW", "source": "https://vis-www.cs.umass.edu/lfw/", "access": "public research dataset; see source terms", "variant": "sklearn fetch_lfw_people", "identities": int(len(dataset.target_names)), "images": int(len(dataset.images)), "local_root": str(args.data_home)}
    Path("data/manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
