"""Build a source-separated key-pool table from tracked compact summaries.

Writes experiments/cross_dataset_key_pool_summary.csv with one row per
(source study, pool) and chance-normalized columns for descriptive comparison.
This is a study-level summary, not a per-seed canonical evidence matrix.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments"

SOURCES = [
    # dataset, partition label, scheme, file, test identities
    ("MOBIO", "A", "BioHash", "mobio_multiexposure/key_pool_boundary_summary.csv", 30),
    ("MOBIO", "A", "BioHash", "mobio_multiexposure/random_key_pool_confirmation_summary.csv", 30),
    ("MOBIO", "B", "BioHash", "mobio_multiexposure/key_pool_split_replication_summary.csv", 30),
    ("MOBIO", "A", "BioHash", "mobio_multiexposure/dense_key_pool_sweep_summary.csv", 30),
    ("MOBIO", "2", "BioHash", "mobio_multiexposure/dense_key_pool_sweep_partition2_summary.csv", 30),
    ("MOBIO", "3", "BioHash", "mobio_multiexposure/dense_key_pool_sweep_partition3_summary.csv", 30),
    ("MOBIO", "A", "BioHash (Haar-corrected)", "mobio_multiexposure/haar_corrected_key_pool_summary.csv", 30),
    ("MOBIO", "A", "MLP-Hash", "mobio_multiexposure/mlphash_key_pool_summary.csv", 30),
    ("MOBIO", "A", "MLP-Hash", "mobio_multiexposure/mlphash_key_pool_dense_summary.csv", 30),
    ("LFW", "A", "BioHash", "lfw_multiexposure/key_pool_boundary_summary.csv", 25),
    ("FEI", "A", "BioHash", "fei_multiexposure/key_pool_boundary_summary.csv", 40),
]


def build_table(root: Path = EXP) -> pd.DataFrame:
    frames = []
    for dataset, partition, scheme, rel, n_test in SOURCES:
        path = root / rel
        df = pd.read_csv(path)
        if df.empty or df["condition"].duplicated().any():
            raise ValueError(f"Empty or duplicate conditions in {rel}")
        if not df["condition"].str.fullmatch(r"(?:random|system)_key_pool_[1-9][0-9]*|independent_unseen_keys").all():
            raise ValueError(f"Unknown key condition in {rel}")
        if (df["condition"] == "independent_unseen_keys").sum() != 1:
            raise ValueError(f"Expected one fresh-key endpoint in {rel}")
        metrics = ["top1_mean", "top1_std", "auroc_mean", "eer_mean",
                   "minimum_clustered_lower", "maximum_clustered_upper"]
        if "one_record_top1_mean" in df:
            metrics.append("one_record_top1_mean")
        for metric in metrics:
            values = pd.to_numeric(df[metric], errors="raise")
            if not (np.isfinite(values) & values.between(0, 1)).all():
                raise ValueError(f"Invalid fractional metric {metric} in {rel}")
        if not (df["minimum_clustered_lower"] <= df["maximum_clustered_upper"]).all():
            raise ValueError(f"Reversed interval bounds in {rel}")
        chance = 1.0 / n_test
        df["dataset"] = dataset
        df["partition"] = partition
        df["scheme"] = scheme
        df["test_identities"] = n_test
        df["chance_top1"] = chance
        df["pool_size"] = df["condition"].str.extract(r"_(\d+)$")[0]
        df.loc[df["condition"] == "independent_unseen_keys", "pool_size"] = "fresh"
        df["top1_over_chance_10"] = df["top1_mean"] / chance
        if "one_record_top1_mean" in df:
            df["top1_over_chance_1"] = df["one_record_top1_mean"] / chance
            df["amplification_pp"] = 100 * (df["top1_mean"] - df["one_record_top1_mean"])
        df["interval_excludes_chance"] = df["minimum_clustered_lower"] > chance
        df["source_file"] = rel
        frames.append(df)
    table = pd.concat(frames, ignore_index=True)
    cols = ["dataset", "partition", "scheme", "pool_size", "test_identities", "chance_top1",
            "one_record_top1_mean", "top1_mean", "top1_std", "auroc_mean", "eer_mean",
            "minimum_clustered_lower", "maximum_clustered_upper", "top1_over_chance_1", "top1_over_chance_10",
            "amplification_pp", "interval_excludes_chance", "source_file"]
    table = table[[c for c in cols if c in table]]
    if table.duplicated(["source_file", "pool_size"]).any():
        raise ValueError("Duplicate study/pool rows")
    return table


def main() -> None:
    table = build_table()
    out = EXP / "cross_dataset_key_pool_summary.csv"
    table.to_csv(out, index=False, float_format="%.6f", lineterminator="\n")
    print(f"{len(table)} rows -> {out}")

if __name__ == "__main__":
    main()
