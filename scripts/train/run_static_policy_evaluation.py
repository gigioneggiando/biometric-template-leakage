"""Evaluate a static policy recommendation using matched, newly trained attackers."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
from scipy.stats import permutation_test
import torch
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from biometrics_ai.protection.policy import analyse_policy, recommend_fresh_policy
from scripts.train.run_scheme_extension_pilot import run_pilots, write_table
from scripts.train.run_scheme_followup import crossed_interval, holm_adjust


def paired_effect(before: dict, after: dict, analysis: dict) -> dict:
    before_by_seed = {run["seed"]: run["identity_top1_scores"] for run in before["runs"]}
    after_by_seed = {run["seed"]: run["identity_top1_scores"] for run in after["runs"]}
    if (len(before_by_seed) != len(before["runs"]) or len(after_by_seed) != len(after["runs"])
            or before_by_seed.keys() != after_by_seed.keys() or len(before_by_seed) < 2):
        raise ValueError("Unique, matched model seeds are required")
    identities = sorted(next(iter(before_by_seed.values())))
    if any(set(scores) != set(identities) for scores in [*before_by_seed.values(), *after_by_seed.values()]):
        raise ValueError("Identity scores must align across policies and seeds")
    seeds = sorted(before_by_seed)
    before_scores = np.asarray([[before_by_seed[seed][identity] for identity in identities] for seed in seeds])
    after_scores = np.asarray([[after_by_seed[seed][identity] for identity in identities] for seed in seeds])
    if not all(np.isfinite(scores).all() and np.all((scores >= 0) & (scores <= 1))
               for scores in (before_scores, after_scores)):
        raise ValueError("Identity scores must be finite probabilities")
    difference = before_scores - after_scores
    lower, upper = crossed_interval(difference, analysis["seed"], analysis["bootstrap_resamples"])
    after_lower, after_upper = crossed_interval(after_scores, analysis["seed"], analysis["bootstrap_resamples"])
    probability = float(permutation_test(
        (difference.mean(axis=0),), np.mean, permutation_type="samples", vectorized=True,
        alternative="greater", n_resamples=analysis["permutations"],
        rng=np.random.default_rng(analysis["seed"])).pvalue)
    return {"before_top1": float(before_scores.mean()), "after_top1": float(after_scores.mean()),
            "reduction": float(difference.mean()), "lower95": lower, "upper95": upper,
            "after_lower95": after_lower, "after_upper95": after_upper,
            "signflip_p": probability, "model_seeds": len(seeds), "identity_clusters": len(identities),
            "chance": 1 / len(identities)}


def analyse_results(config: dict) -> list[dict]:
    rows = []
    for dataset in config["datasets"]:
        for scheme in config["schemes"]:
            study = f"{dataset['name']}_{scheme['protection']['scheme']}_split{dataset['split_reassignment_seed']}"
            directory = Path(config["output_root"]) / study
            before = json.loads((directory / "random_key_pool_4/metrics.json").read_text())
            after = json.loads((directory / "independent_unseen_keys/metrics.json").read_text())
            for exposures in config["exposures"]:
                model = "single_mlp" if exposures == 1 else "mean_mlp"
                baseline = before["conditions"]["random_key_pool_4"]["exposures"][str(exposures)]["models"][model]
                candidate = after["conditions"]["independent_unseen_keys"]["exposures"][str(exposures)]["models"][model]
                effect = paired_effect(baseline, candidate, config["analysis"])
                primary = exposures == 10
                rows.append({"dataset": dataset["name"], "split_seed": dataset["split_reassignment_seed"],
                             "scheme": scheme["name"], "exposures": exposures, "model": model, **effect,
                             "primary": primary, "holm_p": None})
    primary_rows = [row for row in rows if row["primary"]]
    if len(primary_rows) != config["analysis"]["primary_family_size"]:
        raise ValueError("Primary family is incomplete")
    for row, probability in zip(primary_rows, holm_adjust(
            [row["signflip_p"] for row in primary_rows], config["analysis"]["primary_family_size"])):
        row["holm_p"] = probability
    write_table(Path(config["summary_dir"]) / "policy_effects.csv", rows)
    return rows


def execute(config_path: Path) -> dict:
    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    if config["conditions"] != ["random_key_pool_4"]:
        raise ValueError("This matched evaluation requires a pool-of-four baseline")
    if config["models"] != ["mean_mlp"] or config["exposures"] != [1, 10]:
        raise ValueError("The frozen evaluation requires single-record and ten-record mean-pool endpoints")
    baseline = analyse_policy(config)
    candidate = recommend_fresh_policy(config)
    candidate_audit = analyse_policy(candidate)
    if candidate_audit["decision"] == "block":
        raise ValueError("Candidate retains a blocking policy finding")
    destination = Path(config["summary_dir"])
    if destination.exists() or Path(config["output_root"]).exists():
        raise FileExistsError("Use new result and summary directories; prior studies are immutable")
    input_paths = sorted({Path(dataset["embedding_dir"]) / filename for dataset in config["datasets"]
                          for filename in ("embeddings.npy", "metadata.json", "embedding_manifest.json")})
    input_hashes = {path.as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in input_paths}
    sources = sorted(set([config_path.resolve(), ROOT / f"docs/protocols/{config_path.stem}.md"] +
                         list((ROOT / "src/biometrics_ai").rglob("*.py")) + list((ROOT / "scripts/train").glob("*.py"))))
    manifest = {"started_utc": datetime.now(timezone.utc).isoformat(), "status": "running",
                "base_commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip(),
                "dirty_worktree": bool(subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True).stdout.strip()),
                "source_sha256": {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
                "input_sha256": input_hashes, "budget_seconds": config["max_wall_seconds"], "torch_threads": 8,
                "software": {name: version(name) for name in ("numpy", "torch", "scipy", "scikit-learn", "PyYAML")},
                "freeze_method": "pre-execution source, protocol, config and input hashes; no new Git commit"}
    destination.mkdir(parents=True)
    manifest_path = destination / "execution_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    (destination / "policy_audit.json").write_text(json.dumps({"baseline": baseline, "candidate": candidate_audit}, indent=2) + "\n")
    (destination / "recommended_policy.yaml").write_text(yaml.safe_dump(candidate, sort_keys=True))
    evaluation = copy.deepcopy(config)
    evaluation["conditions"] += candidate["conditions"]
    (destination / "executed_matrix.yaml").write_text(yaml.safe_dump(evaluation, sort_keys=True))
    started = time.monotonic()
    torch.set_num_threads(8)
    try:
        status = run_pilots(evaluation)
        if not status["all_cells_complete"]:
            manifest["status"] = "partial"
            raise RuntimeError("Incomplete matrix; no complete-effect claim can be made")
        effects = analyse_results(evaluation)
        manifest["status"] = "completed"
        manifest["completed_cells"] = status["completed_cells"]
        manifest["primary_contrasts"] = sum(row["primary"] for row in effects)
        return manifest
    except Exception:
        if manifest["status"] == "running":
            manifest["status"] = "failed"
        raise
    finally:
        manifest["wall_seconds"] = time.monotonic() - started
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "configs/attacks/static_policy_2026-09-25.yaml")
    args = parser.parse_args()
    manifest = execute(args.config)
    print(json.dumps({key: manifest[key] for key in ("status", "wall_seconds", "completed_cells", "primary_contrasts")}, indent=2))


if __name__ == "__main__":
    main()