"""Create a deterministic identity-disjoint protocol from authorized MOBIO still images."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from biometrics_ai.data.mobio import MobioProtocolConfig, build_mobio_protocol


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-root", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/interim/mobio_multiexposure_protocol.csv"))
    parser.add_argument("--identities", type=int, default=150)
    parser.add_argument("--samples-per-identity", type=int, default=12)
    parser.add_argument("--seed", type=int, default=20260904)
    args = parser.parse_args()

    config = MobioProtocolConfig(args.identities, args.samples_per_identity, args.seed)
    rows = build_mobio_protocol(args.image_root, config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["sample_id", "identity_id", "source_image", "split", "sample_index", "session_id"]
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    split_samples = Counter(str(row["split"]) for row in rows)
    split_identities = {
        split: len({str(row["identity_id"]) for row in rows if row["split"] == split})
        for split in ("train", "val", "test")
    }
    summary = {
        "dataset": "MOBIO selected still images",
        "classification": "independent multi-exposure study; not benchmark_cb reproduction",
        "seed": config.seed,
        "identities": config.identities,
        "samples_per_identity": config.samples_per_identity,
        "sampling": "one randomly selected still per session",
        "split_identities": split_identities,
        "split_samples": dict(split_samples),
        "protocol_csv": args.output.as_posix(),
    }
    args.output.with_suffix(".json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()