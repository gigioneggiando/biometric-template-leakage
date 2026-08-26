"""Run crossed identity-split, key, and model seeds for Month 1 baselines."""
from __future__ import annotations

import argparse
import copy
import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from scripts.train.run_lfw_month1 import (  # noqa: E402
    evaluate_experiment,
    load_embeddings,
    protect_embeddings,
    resplit_metadata,
    write_result,
)


RUN_FIELDS = (
    "study",
    "identity_split_seed",
    "key_seed",
    "model_seed",
    "condition",
    "gallery_identities",
    "probe_samples",
    "chance_top1",
    "top1_linkage",
    "clustered_lower",
    "clustered_upper",
    "auroc",
    "eer",
)

CELL_FIELDS = (
    "study",
    "identity_split_seed",
    "key_seed",
    "condition",
    "model_runs",
    "chance_top1",
    "top1_mean",
    "top1_std",
    "top1_min",
    "top1_max",
    "auroc_mean",
    "eer_mean",
    "all_clustered_intervals_include_chance",
)


def write_csv(path: Path, fieldnames: tuple[str, ...], rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summarize_cells(run_rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, int, int, str], list[dict]] = defaultdict(list)
    for row in run_rows:
        key = (
            str(row["study"]),
            int(row["identity_split_seed"]),
            int(row["key_seed"]),
            str(row["condition"]),
        )
        grouped[key].append(row)

    cells = []
    for (study, split_seed, key_seed, condition), rows in sorted(grouped.items()):
        top1 = np.asarray([float(row["top1_linkage"]) for row in rows])
        chance = float(rows[0]["chance_top1"])
        cells.append(
            {
                "study": study,
                "identity_split_seed": split_seed,
                "key_seed": key_seed,
                "condition": condition,
                "model_runs": len(rows),
                "chance_top1": chance,
                "top1_mean": float(top1.mean()),
                "top1_std": float(top1.std(ddof=1)) if len(top1) > 1 else 0.0,
                "top1_min": float(top1.min()),
                "top1_max": float(top1.max()),
                "auroc_mean": float(np.mean([float(row["auroc"]) for row in rows])),
                "eer_mean": float(np.mean([float(row["eer"]) for row in rows])),
                "all_clustered_intervals_include_chance": all(
                    float(row["clustered_lower"]) <= chance <= float(row["clustered_upper"])
                    for row in rows
                ),
            }
        )
    return cells


def summarize_studies(cell_rows: list[dict]) -> list[dict]:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in cell_rows:
        grouped[(str(row["study"]), str(row["condition"]))].append(row)

    summaries = []
    for (study, condition), rows in sorted(grouped.items()):
        cell_top1 = np.asarray([float(row["top1_mean"]) for row in rows])
        summaries.append(
            {
                "study": study,
                "condition": condition,
                "factorial_cells": len(rows),
                "model_runs_per_cell": int(rows[0]["model_runs"]),
                "chance_top1": float(rows[0]["chance_top1"]),
                "cell_top1_mean": float(cell_top1.mean()),
                "cell_top1_std": float(cell_top1.std(ddof=1)) if len(cell_top1) > 1 else 0.0,
                "cell_top1_min": float(cell_top1.min()),
                "cell_top1_max": float(cell_top1.max()),
                "all_run_clustered_intervals_include_chance": all(
                    bool(row["all_clustered_intervals_include_chance"]) for row in rows
                ),
            }
        )
    return summaries


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    robustness_config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    classification = robustness_config.get("classification")
    if classification != "engineering validation, not benchmark_cb reproduction":
        raise ValueError("Robustness runs must retain the engineering-validation classification")

    output_root = Path(robustness_config["output_root"])
    output_root.mkdir(parents=True, exist_ok=True)
    run_rows: list[dict] = []
    for study in robustness_config["studies"]:
        study_name = str(study["name"])
        base_config_path = Path(study["base_config"])
        base_config = yaml.safe_load(base_config_path.read_text(encoding="utf-8"))
        if base_config.get("classification") != classification:
            raise ValueError(f"Classification mismatch in {base_config_path}")
        embeddings, metadata, embedding_manifest = load_embeddings(Path(base_config["embedding_dir"]))

        key_scope = str(robustness_config.get("independent_key_scope", "sample_id"))
        if key_scope != "sample_id":
            raise ValueError("Crossed robustness requires sample_id keys to keep split and key factors separate")
        sample_order = tuple(str(row["sample_id"]) for row in metadata)
        if len(set(sample_order)) != len(sample_order):
            raise ValueError(f"Duplicate sample IDs in {study_name}")
        for key_seed in robustness_config["key_seeds"]:
            config = copy.deepcopy(base_config)
            config["key_seed"] = int(key_seed)
            config["independent_key_scope"] = key_scope
            precomputed_templates = {
                condition: protect_embeddings(
                    embeddings,
                    metadata,
                    condition,
                    int(key_seed),
                    int(config["template_dim"]),
                    key_scope,
                )[0]
                for condition in config["conditions"]
            }
            for split_seed in robustness_config["identity_split_seeds"]:
                resplit = resplit_metadata(metadata, int(split_seed))
                if tuple(str(row["sample_id"]) for row in resplit) != sample_order:
                    raise RuntimeError("Identity resplitting changed sample order and invalidated cached templates")
                config["results_dir"] = (
                    output_root / study_name / f"split_{int(split_seed)}" / f"key_{int(key_seed)}"
                ).as_posix()
                result = evaluate_experiment(
                    config,
                    embeddings,
                    resplit,
                    embedding_manifest,
                    precomputed_templates=precomputed_templates,
                )
                result["robustness"] = {
                    "identity_split_seed": int(split_seed),
                    "key_seed": int(key_seed),
                    "independent_key_scope": key_scope,
                    "base_config": base_config_path.as_posix(),
                }
                write_result(config, result)
                print(
                    f"Completed {study_name} split={int(split_seed)} key={int(key_seed)}",
                    flush=True,
                )

                for condition, condition_result in result["conditions"].items():
                    for run in condition_result["attacker_runs"]:
                        interval = run["top1_identity_clustered_interval"]
                        run_rows.append(
                            {
                                "study": study_name,
                                "identity_split_seed": int(split_seed),
                                "key_seed": int(key_seed),
                                "model_seed": int(run["seed"]),
                                "condition": condition,
                                "gallery_identities": int(result["gallery_identities"]),
                                "probe_samples": int(result["probe_samples"]),
                                "chance_top1": float(result["chance_top1"]),
                                "top1_linkage": float(run["top1_linkage"]),
                                "clustered_lower": float(interval["lower"]),
                                "clustered_upper": float(interval["upper"]),
                                "auroc": float(run["auroc"]),
                                "eer": float(run["eer"]),
                            }
                        )

    cell_rows = summarize_cells(run_rows)
    summary = {
        "classification": classification,
        "identity_split_seeds": [int(seed) for seed in robustness_config["identity_split_seeds"]],
        "key_seeds": [int(seed) for seed in robustness_config["key_seeds"]],
        "independent_key_scope": str(robustness_config["independent_key_scope"]),
        "runs": len(run_rows),
        "cells": len(cell_rows),
        "studies": summarize_studies(cell_rows),
    }
    write_csv(output_root / "runs.csv", RUN_FIELDS, run_rows)
    write_csv(output_root / "cells.csv", CELL_FIELDS, cell_rows)
    (output_root / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()