"""Prospective trusted-verifier utility confirmation on MOBIO and SCface."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
from threadpoolctl import threadpool_limits


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from biometrics_ai.evaluation.security_utility import paired_mean_interval
from scripts.train import run_source_security_utility as pilot
from scripts.train.run_scheme_extension_pilot import write_table


STUDY = ROOT / "experiments/scface_utility_confirmation_2026-09-25"
PRIVATE = ROOT / "results/scface_utility_confirmation_2026-09-25"
DATASETS = {
    "MOBIO": "mobio/buffalo_l_yunet",
    "SCface": "scface_multiexposure/buffalo_l_yunet",
}
SEEDS = [92927, 92941, 92951, 92957, 92959, 92987, 92993, 93001, 93047, 93053, 93059, 93077]
SPLITS = [93083, 93089]
ALPHA = 0.05 / 8


def compare(before: list[dict], after: list[dict]) -> dict:
    before = sorted(before, key=lambda item: item["master_seed"])
    after = sorted(after, key=lambda item: item["master_seed"])
    if [item["master_seed"] for item in before] != SEEDS or [item["master_seed"] for item in after] != SEEDS:
        raise ValueError("All twelve planned seed pairs are required")
    identities = before[0]["utility"]["identities"]
    if any(item["utility"]["identities"] != identities for item in before + after):
        raise ValueError("Paired identity order differs")
    baseline = np.asarray([item["utility"]["identity_tar"] for item in before])
    candidate = np.asarray([item["utility"]["identity_tar"] for item in after])
    fmr = np.asarray([item["utility"]["identity_fmr"] for item in after])
    tar_lower, tar_upper = paired_mean_interval(candidate - baseline, 93103, 20000, ALPHA)
    _, fmr_upper = paired_mean_interval(fmr, 93103, 20000, ALPHA)
    return {
        "baseline_tar": float(baseline.mean()),
        "candidate_tar": float(candidate.mean()),
        "tar_difference": float((candidate - baseline).mean()),
        "tar_lower": tar_lower,
        "tar_upper": tar_upper,
        "candidate_fmr": float(fmr.mean()),
        "fmr_upper": fmr_upper,
        "margin": 0.03,
        "fmr_limit": 0.02,
        "tail_alpha": ALPHA,
        "utility_pass": tar_lower >= -0.03 and fmr_upper <= 0.02,
        "identity_clusters": len(identities),
        "key_seeds": len(before),
    }


def execute(data_root: Path) -> dict:
    outputs = ["execution_manifest.json", "endpoints.csv", "effects.csv"]
    existing = [name for name in outputs if (STUDY / name).exists()]
    if existing or PRIVATE.exists():
        raise FileExistsError(f"Refusing to overwrite utility outputs: {existing}")
    inputs = {
        f"{dataset}/{name}": data_root / directory / name
        for dataset, directory in DATASETS.items()
        for name in ("embeddings.npy", "metadata.json", "embedding_manifest.json")
    }
    missing = [str(path) for path in inputs.values() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"Missing utility inputs: {missing}")
    sources = [
        Path(__file__),
        ROOT / "scripts/train/run_source_security_utility.py",
        ROOT / "src/biometrics_ai/evaluation/security_utility.py",
        ROOT / "docs/protocols/scface_utility_confirmation_2026-09-25.md",
    ]
    manifest = {
        "status": "running",
        "started_utc": datetime.now(timezone.utc).isoformat(),
        "base_commit": subprocess.run(
            ["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True
        ).stdout.strip(),
        "source_sha256": {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
        "input_sha256": {name: hashlib.sha256(path.read_bytes()).hexdigest() for name, path in inputs.items()},
        "software": {name: version(name) for name in ("numpy", "scipy", "threadpoolctl")},
        "datasets": DATASETS,
        "key_seeds": SEEDS,
        "split_seeds": SPLITS,
        "planned_evaluations": 96,
        "attacker_training_runs": 0,
        "budget_seconds": 3600,
        "utility_margin": 0.03,
        "fmr_limit": 0.02,
        "tail_alpha": ALPHA,
    }
    PRIVATE.mkdir(parents=True)
    manifest_path = STUDY / "execution_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    started = time.monotonic()
    records, endpoints, effects = [], [], []
    try:
        with threadpool_limits(limits=1):
            for dataset, directory in DATASETS.items():
                embeddings, original, _ = pilot.runner.load_embeddings(data_root / directory)
                if not np.isfinite(embeddings).all() or not np.allclose(
                    np.linalg.norm(embeddings, axis=1), 1, atol=1e-4
                ):
                    raise ValueError("Finite unit embeddings required")
                counts = {identity: 0 for identity in {str(row["identity_id"]) for row in original}}
                for row in original:
                    counts[str(row["identity_id"])] += 1
                if min(counts.values()) < 2:
                    raise ValueError("Every identity needs one enrollment and at least one probe")
                for split in SPLITS:
                    metadata = pilot.runner.reassign_identity_splits(original, split)
                    test_identities = {str(row["identity_id"]) for row in metadata if row["split"] == "test"}
                    expected = 30 if dataset == "MOBIO" else 26
                    if len(test_identities) != expected:
                        raise ValueError(f"Unexpected {dataset} test identity count")
                    cell = []
                    for seed in SEEDS:
                        for policy in ("recurring", "separated"):
                            utility = pilot.utility(embeddings, metadata, policy, seed, started + 3600)
                            record = {
                                "dataset": dataset,
                                "split_seed": split,
                                "master_seed": seed,
                                "policy": policy,
                                "utility": utility,
                            }
                            records.append(record)
                            cell.append(record)
                            (PRIVATE / f"{dataset}_{split}_{seed}_{policy}.json").write_text(
                                json.dumps(record, indent=2) + "\n", encoding="utf-8"
                            )
                            endpoints.append(
                                {key: value for key, value in record.items() if key != "utility"}
                                | {key: value for key, value in utility.items()
                                   if key not in {"identities", "identity_tar", "identity_fmr"}}
                            )
                            write_table(STUDY / "endpoints.csv", endpoints)
                    effect = compare(
                        [record for record in cell if record["policy"] == "recurring"],
                        [record for record in cell if record["policy"] == "separated"],
                    )
                    effects.append({"dataset": dataset, "split_seed": split, **effect})
                    write_table(STUDY / "effects.csv", effects)
                    print(
                        f"{dataset} split {split}: TAR {effect['baseline_tar']:.4f} -> "
                        f"{effect['candidate_tar']:.4f}, lower {effect['tar_lower']:.4f}, "
                        f"FMR upper {effect['fmr_upper']:.4f}, pass={effect['utility_pass']}",
                        flush=True,
                    )
        manifest["status"] = "completed"
        manifest["completed_evaluations"] = len(records)
        manifest["utility_passes"] = sum(row["utility_pass"] for row in effects)
        manifest["scface_primary_pass"] = all(
            row["utility_pass"] for row in effects if row["dataset"] == "SCface"
        )
        manifest["all_cells_pass"] = all(row["utility_pass"] for row in effects)
    except Exception:
        manifest["status"] = "failed"
        manifest["completed_evaluations"] = len(records)
        raise
    finally:
        manifest["wall_seconds"] = time.monotonic() - started
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    args = parser.parse_args()
    result = execute(args.data_root.resolve())
    print(json.dumps({key: result[key] for key in (
        "status", "completed_evaluations", "utility_passes", "scface_primary_pass",
        "all_cells_pass", "wall_seconds",
    )}, indent=2))


if __name__ == "__main__":
    main()
