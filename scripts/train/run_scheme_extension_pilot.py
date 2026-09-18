"""Run bounded, resumable scheme pilots and export only non-sensitive summaries."""
from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from scripts.train import run_real_multiexposure as runner
from biometrics_ai.evaluation.metrics import paired_identity_interval, exploratory_equivalence_sensitivity


def write_table(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def export_summaries(completed: list[tuple[dict, dict]], destination: Path) -> None:
    rows, native_rows = [], []
    private_scores = {}
    for cell, result in completed:
        test_identities = result["split_identity_counts"]["test"]
        common = {"stage": cell.get("stage", "pilot"), "dataset": cell["dataset"], "scheme": cell["scheme_label"],
              "split_seed": cell.get("split_reassignment_seed", "original"),
                  "condition": cell["conditions"][0], "test_identities": test_identities,
                  "chance": 1 / test_identities, "key_seed": cell["key_seed"], "set_seed": cell["set_seed"],
                  "config_sha256": result["pilot_config_sha256"], "git_commit": result["git_commit"]}
        condition_result = result["conditions"][common["condition"]]
        diagnostics = condition_result["template_diagnostics"]
        native_rows.append({**common, "input_dimension": diagnostics["input_dimension"],
                            "zero_rows": diagnostics["zero_rows"], "constant_columns": diagnostics["constant_columns"],
                            "native_top1": diagnostics["native_matching"]["top1_linkage"],
                            "native_auroc": diagnostics["native_matching"]["auroc"]})
        for exposures, exposure_result in condition_result["exposures"].items():
            for model, model_result in exposure_result["models"].items():
                for run in model_result["runs"]:
                    interval = run["top1_identity_clustered_interval"]
                    rows.append({**common, "exposures": int(exposures), "model": model, "seed": run["seed"],
                                 "top1": run["top1_linkage"], "top5": run["top5_linkage"], "auroc": run["auroc"],
                                 "eer": run["eer"], "tar_at_far_1e-2": run["tar_at_far_1e-2"],
                                 "tar_at_far_1e-3": run["tar_at_far_1e-3"], "lower95": interval["lower"],
                                 "upper95": interval["upper"], "best_epoch": run["best_epoch"],
                                 "elapsed_seconds": run["elapsed_seconds"],
                                 "oracle_top1": exposure_result["unprotected_oracle"]["top1_linkage"]})
                    key = (common["stage"], common["dataset"], common["split_seed"], common["scheme"], common["condition"], int(exposures), model, run["seed"])
                    private_scores[key] = run["identity_top1_scores"]
    paired, sensitivity = [], []
    for key, target in private_scores.items():
        stage, dataset, split_seed, scheme, condition, exposures, model, seed = key
        common = {"stage": stage, "dataset": dataset, "split_seed": split_seed, "scheme": scheme, "condition": condition,
                  "exposures": exposures, "model": model, "seed": seed}
        references = []
        if exposures == 10:
            references.append(("ten_minus_one", (stage, dataset, split_seed, scheme, condition, 1, "single_mlp", seed)))
        if condition != "independent_unseen_keys":
            references.append(("reuse_minus_fresh", (stage, dataset, split_seed, scheme, "independent_unseen_keys", exposures, model, seed)))
        for contrast, reference_key in references:
            if reference_key in private_scores:
                interval = paired_identity_interval(private_scores[reference_key], target, seed=91223)
                interval["bootstrap_seed"] = interval.pop("seed")
                paired.append({**common, "contrast": contrast, **interval})
        if condition == "independent_unseen_keys":
            sensitivity.extend({**common, **row} for row in exploratory_equivalence_sensitivity(target, 1 / len(target)))
    write_table(destination / "results_summary.csv", rows)
    write_table(destination / "native_utility.csv", native_rows)
    write_table(destination / "paired_uncertainty.csv", paired)
    write_table(destination / "equivalence_sensitivity.csv", sensitivity)


def run_pilots(config: dict, *, resume: bool = False) -> dict:
    if config.get("stage") not in {"pilot", "bounded_validation"} or not 0 < float(config["max_wall_seconds"]) <= 3600:
        raise ValueError("This driver permits only bounded studies with a budget of at most one hour")
    started = time.monotonic()
    deadline = started + float(config["max_wall_seconds"])
    output_root = Path(config["output_root"])
    summary_dir = Path(config["summary_dir"])
    summary_dir.mkdir(parents=True, exist_ok=True)
    completed, states = [], []
    for condition in config["conditions"]:
        for scheme in config["schemes"]:
            for dataset in config["datasets"]:
                cell = {key: copy.deepcopy(value) for key, value in config.items()
                        if key not in {"max_wall_seconds", "output_root", "summary_dir", "datasets", "schemes"}}
                study = f"{dataset['name']}_{scheme['protection']['scheme']}"
                if "split_reassignment_seed" in dataset:
                    cell["split_reassignment_seed"] = int(dataset["split_reassignment_seed"])
                    study += f"_split{cell['split_reassignment_seed']}"
                cell.update(dataset=dataset["name"], embedding_dir=dataset["embedding_dir"],
                            protection=scheme["protection"], scheme_label=scheme["name"], template_dim=scheme["template_dim"],
                            conditions=[condition], results_dir=str(output_root / study / condition))
                fingerprint = hashlib.sha256(yaml.safe_dump(cell, sort_keys=True).encode()).hexdigest()
                metric_path = Path(cell["results_dir"]) / "metrics.json"
                state = {"dataset": dataset["name"], "scheme": scheme["name"], "condition": condition}
                if "split_reassignment_seed" in cell:
                    state["split_seed"] = cell["split_reassignment_seed"]
                if metric_path.exists():
                    if not resume:
                        raise FileExistsError("Pilot outputs exist; use --resume to validate and reuse them")
                    result = json.loads(metric_path.read_text(encoding="utf-8"))
                    if result.get("pilot_config_sha256") != fingerprint:
                        raise ValueError("Existing pilot configuration differs; use a new output directory")
                    completed.append((cell, result))
                    states.append({**state, "status": "reused"})
                    continue
                if time.monotonic() >= deadline:
                    states.append({**state, "status": "not_run_budget"})
                    continue
                print(f"Starting {study} / {condition}", flush=True)
                cell_started = time.monotonic()
                try:
                    embeddings, _, _ = runner.load_embeddings(Path(cell["embedding_dir"]))
                    if not np.isfinite(embeddings).all() or not np.allclose(np.linalg.norm(embeddings, axis=1), 1, atol=1e-4):
                        raise ValueError("Pilot input embeddings must be finite and unit-normalized")
                    execution_cell = copy.deepcopy(cell)
                    execution_cell["training"]["deadline_monotonic"] = deadline
                    result = runner.run(execution_cell)
                    result["pilot_config_sha256"] = fingerprint
                    runner.write_results(cell, result)
                    completed.append((cell, result))
                    states.append({**state, "status": "completed", "elapsed_seconds": time.monotonic() - cell_started})
                    export_summaries(completed, summary_dir)
                    print(f"Completed {study} / {condition} in {time.monotonic() - cell_started:.1f}s", flush=True)
                except (FileNotFoundError, ValueError, RuntimeError, TimeoutError) as error:
                    states.append({**state, "status": "budget_exhausted" if isinstance(error, TimeoutError) else "failed",
                                   "error_type": type(error).__name__})
                    error_path = Path(cell["results_dir"]) / "error.txt"
                    error_path.parent.mkdir(parents=True, exist_ok=True)
                    error_path.write_text(str(error), encoding="utf-8")
                    print(f"Stopped {study} / {condition}: {type(error).__name__}", flush=True)
    export_summaries(completed, summary_dir)
    status = {"stage": config["stage"], "planned_cells": len(states), "completed_cells": len(completed),
              "all_cells_complete": len(completed) == len(states), "wall_seconds": time.monotonic() - started,
              "budget_seconds": float(config["max_wall_seconds"]), "cells": states,
              "model_seeds": config["training"]["seeds"],
              "interpretation": "Bounded independent study; stage and replication are explicit, not proof of equivalence"}
    (summary_dir / "matrix_status.json").write_text(json.dumps(status, indent=2) + "\n", encoding="utf-8")
    return status


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs/attacks/scheme_extension_pilot.yaml")
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    status = run_pilots(yaml.safe_load(args.config.read_text(encoding="utf-8")), resume=args.resume)
    print(json.dumps({key: value for key, value in status.items() if key != "cells"}, indent=2))


if __name__ == "__main__":
    main()