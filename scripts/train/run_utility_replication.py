"""Fixed-size utility-only replication, preserving the failed earlier pilot."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
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

STUDY = ROOT / "experiments/utility_replication_2026-09-25"
PRIVATE = ROOT / "results/utility_replication_2026-09-25"
SEEDS = [92701, 92707, 92717, 92723, 92737, 92753, 92761, 92767, 92779, 92789, 92801, 92809]
SPLITS = [92821, 92831]


def compare(before: list[dict], after: list[dict]) -> dict:
    before = sorted(before, key=lambda item: item["master_seed"])
    after = sorted(after, key=lambda item: item["master_seed"])
    if [item["master_seed"] for item in before] != SEEDS or [item["master_seed"] for item in after] != SEEDS:
        raise ValueError("All twelve planned seed pairs are required")
    identities = before[0]["utility"]["identities"]
    if any(item["utility"]["identities"] != identities for item in before + after):
        raise ValueError("Paired identities differ")
    baseline = np.asarray([item["utility"]["identity_tar"] for item in before])
    candidate = np.asarray([item["utility"]["identity_tar"] for item in after])
    fmr = np.asarray([item["utility"]["identity_fmr"] for item in after])
    lower, upper = paired_mean_interval(candidate - baseline, 92843, 20000, .05 / 8)
    _, fmr_upper = paired_mean_interval(fmr, 92843, 20000, .05 / 8)
    return {"baseline_tar": float(baseline.mean()), "candidate_tar": float(candidate.mean()),
            "tar_difference": float((candidate - baseline).mean()), "tar_lower": lower, "tar_upper": upper,
            "candidate_fmr": float(fmr.mean()), "fmr_upper": fmr_upper,
            "margin": .03, "fmr_limit": .02, "tail_alpha": .05 / 8,
            "utility_pass": lower >= -.03 and fmr_upper <= .02,
            "identity_clusters": len(identities), "key_seeds": len(before)}


def execute() -> dict:
    if STUDY.exists() or PRIVATE.exists():
        raise FileExistsError("Refusing to overwrite replication outputs")
    paths = sorted(set(list((ROOT / "src/biometrics_ai").rglob("*.py")) +
                       list((ROOT / "scripts/train").glob("*.py")) +
                       [ROOT / "scripts/diagnostics/source_policy_recipes.py",
                        ROOT / "docs/protocols/utility_replication_2026-09-25.md"]))
    inputs = [ROOT / directory / filename for directory in pilot.DATASETS.values()
              for filename in ["embeddings.npy", "metadata.json", "embedding_manifest.json"]]
    manifest = {"status": "running", "started_utc": datetime.now(timezone.utc).isoformat(),
                "source_sha256": {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths},
                "input_sha256": {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in inputs},
                "software": {name: version(name) for name in ["numpy", "torch", "scipy", "scikit-learn", "threadpoolctl"]},
                "key_seeds": SEEDS, "split_seeds": SPLITS, "budget_seconds": 3600,
                "planned_evaluations": 96, "attacker_training_runs": 0, "independent_review": "pending"}
    STUDY.mkdir(parents=True)
    PRIVATE.mkdir(parents=True)
    manifest_path = STUDY / "execution_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    started = time.monotonic()
    records, endpoints, effects = [], [], []
    try:
        with threadpool_limits(limits=1):
            for dataset, directory in pilot.DATASETS.items():
                embeddings, original, _ = pilot.runner.load_embeddings(ROOT / directory)
                if not np.isfinite(embeddings).all() or not np.allclose(np.linalg.norm(embeddings, axis=1), 1, atol=1e-4):
                    raise ValueError("Finite unit embeddings required")
                for split in SPLITS:
                    metadata = pilot.runner.reassign_identity_splits(original, split)
                    cell = []
                    for seed in SEEDS:
                        for policy in ["recurring", "separated"]:
                            utility = pilot.utility(embeddings, metadata, policy, seed, started + 3600)
                            record = {"dataset": dataset, "split_seed": split, "master_seed": seed,
                                      "policy": policy, "utility": utility}
                            records.append(record)
                            cell.append(record)
                            (PRIVATE / f"{dataset}_{split}_{seed}_{policy}.json").write_text(json.dumps(record, indent=2) + "\n")
                            endpoints.append({key: value for key, value in record.items() if key != "utility"} |
                                             {key: value for key, value in utility.items() if key not in {"identities", "identity_tar", "identity_fmr"}})
                            write_table(STUDY / "endpoints.csv", endpoints)
                    effect = compare([record for record in cell if record["policy"] == "recurring"],
                                     [record for record in cell if record["policy"] == "separated"])
                    effects.append({"dataset": dataset, "split_seed": split, **effect})
                    write_table(STUDY / "effects.csv", effects)
                    print(f"{dataset} split {split}: TAR {effect['baseline_tar']:.4f} -> {effect['candidate_tar']:.4f}, "
                          f"lower {effect['tar_lower']:.4f}, FMR upper {effect['fmr_upper']:.4f}, pass={effect['utility_pass']}", flush=True)
        manifest["status"] = "completed"
        manifest["utility_passes"] = sum(row["utility_pass"] for row in effects)
    except Exception:
        manifest["status"] = "failed"
        raise
    finally:
        manifest["completed_evaluations"] = len(records)
        manifest["wall_seconds"] = time.monotonic() - started
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    result = execute()
    print(json.dumps({key: result[key] for key in ["status", "completed_evaluations", "utility_passes", "wall_seconds"]}, indent=2))