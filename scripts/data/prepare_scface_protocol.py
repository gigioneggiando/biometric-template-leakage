"""Create the deterministic SCface mugshot-to-surveillance protocol."""
from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

from biometrics_ai.data.scface import ScfaceProtocolConfig, build_scface_protocol


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--image-root", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("data/interim/scface_multiexposure_protocol.csv"))
    parser.add_argument("--identities", type=int, default=130)
    parser.add_argument("--seed", type=int, default=20260918)
    args = parser.parse_args()

    config = ScfaceProtocolConfig(args.identities, args.seed)
    rows = build_scface_protocol(args.image_root, config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    with args.output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    summary = {
        "dataset": "SCface visible mugshot-to-surveillance protocol",
        "classification": "independent multi-exposure study; not benchmark_cb reproduction",
        "seed": config.seed,
        "identities": config.identities,
        "records_per_identity": 22,
        "gallery_records_per_identity": 1,
        "exposure_candidates_per_identity": 21,
        "ir_excluded": True,
        "split_identities": {
            split: len({str(row["identity_id"]) for row in rows if row["split"] == split})
            for split in ("train", "val", "test")
        },
        "split_samples": dict(Counter(str(row["split"]) for row in rows)),
        "protocol_csv": args.output.as_posix(),
    }
    args.output.with_suffix(".json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
