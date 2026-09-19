"""Learned attacker trained on protected templates built from raw (non-unit) ArcFace input.

See docs/protocols/raw_input_attacker_2026-09-19.md, frozen before execution.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from scripts.train import run_real_multiexposure as runner
from scripts.train.run_scheme_extension_pilot import write_table
from scripts.diagnostics.run_norm_native_audit import extract_raw

DESTINATION = ROOT / "experiments/raw_input_attacker_2026-09-19"
RAW_ROOT = ROOT / "results/raw_input_attacker_2026-09-19"
BUDGET_SECONDS = 1800
KEY_SEED = 92201
SET_SEED = 92207
TRAINING = {"seeds": [601, 607, 613], "epochs": 120, "patience": 30, "hidden_dim": 256,
            "learning_rate": 0.001, "weight_decay": 0.0001, "mse_weight": 0.1,
            "bootstrap_resamples": 2000, "bootstrap_confidence": 0.95, "retain_identity_scores": True}
DATASETS = [
    {"name": "MOBIO", "embedding_dir": "data/processed/embeddings/mobio/buffalo_l_yunet"},
    {"name": "SCface", "embedding_dir": "data/processed/embeddings/scface_multiexposure/buffalo_l_yunet"},
]
SCHEMES = [
    {"name": "PolyProtect", "template_dim": 170,
     "protection": {"scheme": "polyprotect_paper_specified", "window_size": 5, "overlap": 2, "coefficient_bound": 50}},
    {"name": "IoM-GRP", "template_dim": 4800,
     "protection": {"scheme": "iomgrp_paper_specified", "groups": 300, "group_size": 16}},
]
CONDITIONS = ["independent_unseen_keys", "random_key_pool_4"]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def materialize_raw_directory(dataset: dict, deadline: float) -> Path:
    raw, unit, metadata, audit = extract_raw(dataset, deadline)
    del unit
    destination = RAW_ROOT / f"{dataset['name']}_embeddings" / "buffalo_l_yunet"
    destination.mkdir(parents=True, exist_ok=True)
    np.save(destination / "embeddings.npy", raw.astype(np.float32))
    source_directory = ROOT / dataset["embedding_dir"]
    (destination / "metadata.json").write_text((source_directory / "metadata.json").read_text(encoding="utf-8"), encoding="utf-8")
    manifest = json.loads((source_directory / "embedding_manifest.json").read_text(encoding="utf-8"))
    manifest["raw_non_unit_normalized"] = True
    manifest["raw_extraction_audit"] = audit
    (destination / "embedding_manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Raw embeddings materialized: {dataset['name']} ({len(raw)} records, "
          f"norm {audit['raw_norm_min']:.2f}-{audit['raw_norm_max']:.2f})", flush=True)
    return destination


def run_cell(dataset_name: str, embedding_dir: Path, scheme: dict, condition: str, deadline: float) -> dict:
    results_dir = ROOT / "results/raw_input_attacker_2026-09-19" / f"{dataset_name}_{scheme['name']}" / condition
    config = {
        "classification": "exploratory independent study, not benchmark_cb reproduction",
        "stage": "bounded_validation",
        "dataset": dataset_name,
        "embedding_dir": str(embedding_dir.relative_to(ROOT)),
        "conditions": [condition],
        "primary_analysis": "descriptive_control",
        "control_model": "mean_mlp",
        "control_name": "raw_input_attacker_2026-09-19",
        "key_seed": KEY_SEED,
        "set_seed": SET_SEED,
        "template_dim": scheme["template_dim"],
        "protection": scheme["protection"],
        "repeats_per_identity": 8,
        "exposures": [1, 10],
        "models": ["mean_mlp", "deepsets"],
        "record_template_diagnostics": False,
        "training": {**TRAINING, "deadline_monotonic": deadline},
        "results_dir": str(results_dir),
    }
    result = runner.run(config)
    runner.write_results(config, result)
    return result


def summarize(result: dict, dataset_name: str, scheme_name: str, condition: str, rows: list[dict]) -> None:
    for exposure, exposure_result in result["conditions"][condition]["exposures"].items():
        for model, model_result in exposure_result["models"].items():
            summary = model_result["summary"]["top1_linkage"]
            rows.append({"dataset": dataset_name, "scheme": scheme_name, "condition": condition,
                         "exposures": int(exposure), "model": model,
                         "chance": 1 / result["split_identity_counts"]["test"],
                         "top1_mean": summary["mean"], "top1_std": summary["std"],
                         "model_seeds": len(model_result["runs"])})


def execute() -> None:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    manifest_path = DESTINATION / "execution_manifest.json"
    if manifest_path.exists():
        raise FileExistsError("Existing study freeze will not be overwritten")
    sources = [Path(__file__), ROOT / "docs/protocols/raw_input_attacker_2026-09-19.md",
               ROOT / "scripts/diagnostics/run_norm_native_audit.py",
               ROOT / "scripts/train/run_real_multiexposure.py"]
    manifest = {"started_utc": datetime.now(timezone.utc).isoformat(), "budget_seconds": BUDGET_SECONDS,
                "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "dirty_worktree": bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)),
                "source_sha256": {path.relative_to(ROOT).as_posix(): digest(path) for path in sources},
                "key_seed": KEY_SEED, "set_seed": SET_SEED, "datasets": [d["name"] for d in DATASETS],
                "schemes": [s["name"] for s in SCHEMES], "conditions": CONDITIONS}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    started = time.monotonic()
    deadline = started + BUDGET_SECONDS
    rows: list[dict] = []
    try:
        for dataset in DATASETS:
            raw_directory = materialize_raw_directory(dataset, min(deadline, time.monotonic() + 600))
            for scheme in SCHEMES:
                for condition in CONDITIONS:
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Study budget exhausted")
                    print(f"Starting {dataset['name']} / {scheme['name']} / {condition}", flush=True)
                    cell_started = time.monotonic()
                    result = run_cell(dataset["name"], raw_directory, scheme, condition, deadline)
                    summarize(result, dataset["name"], scheme["name"], condition, rows)
                    print(f"Completed {dataset['name']} / {scheme['name']} / {condition} in "
                          f"{time.monotonic() - cell_started:.1f}s", flush=True)
        manifest["status"] = "completed"
    except Exception:
        manifest["status"] = "failed_or_incomplete"
        raise
    finally:
        write_table(DESTINATION / "raw_input_results.csv", rows)
        manifest["wall_seconds"] = round(time.monotonic() - started, 3)
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        print("Study status:", manifest["status"], "seconds:", manifest["wall_seconds"], flush=True)


if __name__ == "__main__":
    execute()
