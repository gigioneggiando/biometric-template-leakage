"""Create a deterministic identity-disjoint CFP Month 1 protocol."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from biometrics_ai.data.cfp import CfpProtocolConfig, build_cfp_protocol


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--image-root",
        type=Path,
        default=Path("data/raw/cfp/cfp-dataset/Data/Images"),
    )
    parser.add_argument("--output", type=Path, default=Path("data/interim/cfp_month1_protocol.csv"))
    parser.add_argument("--identities", type=int, default=500)
    parser.add_argument("--samples-per-identity", type=int, default=10)
    parser.add_argument("--seed", type=int, default=20260826)
    parser.add_argument("--views", nargs="+", choices=("frontal", "profile"), default=["frontal"])
    args = parser.parse_args()

    config = CfpProtocolConfig(
        identities=args.identities,
        samples_per_identity=args.samples_per_identity,
        seed=args.seed,
        views=tuple(args.views),
    )
    rows = build_cfp_protocol(args.image_root, config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=["sample_id", "identity_id", "source_image", "split", "sample_index", "view"],
        )
        writer.writeheader()
        writer.writerows(rows)

    split_samples = Counter(str(row["split"]) for row in rows)
    split_identities = {
        split: len({str(row["identity_id"]) for row in rows if row["split"] == split})
        for split in ("train", "val", "test")
    }
    summary = {
        "dataset": f"CFP {'+'.join(config.views)}",
        "classification": "engineering validation, not benchmark_cb reproduction",
        "seed": config.seed,
        "identities": config.identities,
        "samples_per_identity": config.samples_per_identity,
        "views": list(config.views),
        "split_identities": split_identities,
        "split_samples": dict(split_samples),
        "protocol_csv": args.output.as_posix(),
    }
    args.output.with_suffix(".json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()