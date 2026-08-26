"""Create a deterministic identity-disjoint Olivetti Month 1 protocol."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from biometrics_ai.data.olivetti import OlivettiProtocolConfig, build_olivetti_protocol


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-root", type=Path, default=Path("data/raw/olivetti/images"))
    parser.add_argument("--output", type=Path, default=Path("data/interim/olivetti_month1_protocol.csv"))
    parser.add_argument("--identities", type=int, default=40)
    parser.add_argument("--samples-per-identity", type=int, default=10)
    parser.add_argument("--seed", type=int, default=20260826)
    args = parser.parse_args()

    config = OlivettiProtocolConfig(args.identities, args.samples_per_identity, args.seed)
    rows = build_olivetti_protocol(args.image_root, config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["sample_id", "identity_id", "source_image", "split", "sample_index"],
        )
        writer.writeheader()
        writer.writerows(rows)

    split_samples = Counter(str(row["split"]) for row in rows)
    split_identities = {
        split: len({str(row["identity_id"]) for row in rows if row["split"] == split})
        for split in ("train", "val", "test")
    }
    summary = {
        "dataset": "Olivetti faces",
        "classification": "engineering validation, not benchmark_cb reproduction",
        "seed": config.seed,
        "identities": config.identities,
        "samples_per_identity": config.samples_per_identity,
        "split_identities": split_identities,
        "split_samples": dict(split_samples),
        "protocol_csv": args.output.as_posix(),
    }
    args.output.with_suffix(".json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()