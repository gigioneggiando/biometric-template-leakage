"""Build the canonical cross-dataset key-pool table from tracked compact summaries.

Writes experiments/cross_dataset_key_pool_summary.csv with one row per
(dataset, partition, scheme, pool) and chance-normalized columns so that
galleries of different sizes can be compared.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
EXP = ROOT / "experiments"

SOURCES = [
    # dataset, partition label, scheme, file, test identities
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


def main() -> None:
    frames = []
    for dataset, partition, scheme, rel, n_test in SOURCES:
        path = EXP / rel
        if not path.exists():
            continue
        df = pd.read_csv(path)
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
            "minimum_clustered_lower", "top1_over_chance_1", "top1_over_chance_10",
            "amplification_pp", "interval_excludes_chance", "source_file"]
    table = table[[c for c in cols if c in table]]
    out = EXP / "cross_dataset_key_pool_summary.csv"
    table.to_csv(out, index=False, float_format="%.6f", lineterminator="\n")
    print(f"{len(table)} rows -> {out}")

    # concise view for the README
    view = table[table["scheme"] == "BioHash"].pivot_table(
        index="pool_size", columns=["dataset", "partition"], values="top1_mean", aggfunc="first"
    )
    order = [str(k) for k in (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)] + ["fresh"]
    view = view.reindex([p for p in order if p in view.index])
    print((100 * view).round(1).to_string())


if __name__ == "__main__":
    main()
