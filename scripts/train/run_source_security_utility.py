"""Matched leakage and trusted-verifier utility evaluation of executable policies."""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
import torch
from threadpoolctl import threadpool_limits

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from biometrics_ai.data.multiexposure import ExposureSetConfig, build_real_exposure_sets
from biometrics_ai.evaluation.security_utility import acceptance_gate, paired_mean_interval, validation_threshold
from biometrics_ai.protection.biohash import BioHashConfig, _orthonormal_projection, _correlated_orthonormal_projection
from biometrics_ai.protection.source_analysis import analyse_source
from scripts.diagnostics import source_policy_recipes as recipes
from scripts.diagnostics.benchmark_source_analysis import evaluate as benchmark
from scripts.train import run_real_multiexposure as runner
from scripts.train.run_scheme_extension_pilot import write_table

STUDY = ROOT / "experiments/source_security_utility_2026-09-25"
PRIVATE = ROOT / "results/source_security_utility_2026-09-25"
DATASETS = {"MOBIO": "data/processed/embeddings/mobio/buffalo_l_yunet",
            "FEI": "data/processed/embeddings/fei_multiexposure/buffalo_l_yunet"}
MASTER_SEEDS = [92603, 92609, 92617]
MODEL_SEEDS = [811, 821, 823]
POLICIES = ["recurring", "partial", "separated"]
CONFIG = BioHashConfig(512, 64, haar_sign_corrected=True)
TRAINING = {"hidden_dim": 256, "learning_rate": .001, "weight_decay": .0001, "epochs": 120,
            "patience": 30, "mse_weight": .1, "bootstrap_resamples": 2000,
            "bootstrap_confidence": .95, "retain_identity_scores": True}


def projection(policy: str, master: int, record_id: int) -> np.ndarray:
    if policy == "recurring":
        return _orthonormal_projection(512, 64, recipes.pool_key(master, record_id), True)
    if policy == "separated":
        return _orthonormal_projection(512, 64, recipes.fresh_key(master, record_id), True)
    if policy == "partial":
        return _correlated_orthonormal_projection(512, 64, recipes.common_key(master),
                                                  recipes.fresh_key(master, record_id), 16, True)
    raise ValueError("Unknown executable policy")


def protect(embeddings: np.ndarray, policy: str, master: int, deadline: float) -> np.ndarray:
    templates = []
    for record_id, embedding in enumerate(embeddings):
        if time.monotonic() >= deadline:
            raise TimeoutError("Study wall-clock budget exhausted")
        templates.append((embedding @ projection(policy, master, record_id) >= 0).astype(np.uint8))
    values = np.asarray(templates)
    for record_id in [0, len(embeddings) // 2, len(embeddings) - 1]:
        direct = getattr(recipes, policy)(embeddings[record_id], master, record_id, CONFIG)
        np.testing.assert_array_equal(values[record_id], direct)
    return values


def verification_scores(embeddings: np.ndarray, metadata: list[dict], split: str,
                        policy: str, master: int, deadline: float) -> dict:
    identities = sorted({str(row["identity_id"]) for row in metadata if row["split"] == split})
    groups = [[index for index, row in enumerate(metadata) if row["split"] == split and str(row["identity_id"]) == identity]
              for identity in identities]
    groups = [sorted(group, key=lambda index: int(metadata[index]["sample_index"])) for group in groups]
    enrollment = [group[0] for group in groups]
    probe_indices = [index for group in groups for index in group[1:]]
    labels = np.asarray([label for label, group in enumerate(groups) for _ in group[1:]])
    scores = np.empty((len(probe_indices), len(enrollment)))
    for label, record_id in enumerate(enrollment):
        if time.monotonic() >= deadline:
            raise TimeoutError("Verification wall-clock budget exhausted")
        transform = projection(policy, master, record_id)
        gallery = embeddings[record_id] @ transform >= 0
        probes = embeddings[probe_indices] @ transform >= 0
        scores[:, label] = np.mean(probes == gallery, axis=1)
    matches = labels[:, None] == np.arange(len(enrollment))[None, :]
    return {"scores": scores, "matches": matches, "labels": labels, "identities": identities}


def utility(embeddings: np.ndarray, metadata: list[dict], policy: str, master: int, deadline: float) -> dict:
    validation = verification_scores(embeddings, metadata, "val", policy, master, deadline)
    threshold = validation_threshold(validation["scores"][~validation["matches"]], .01)
    test = verification_scores(embeddings, metadata, "test", policy, master, deadline)
    accepted = test["scores"] >= threshold
    true_accept, false_match = [], []
    for label in range(len(test["identities"])):
        selected = test["labels"] == label
        true_accept.append(float(accepted[selected][test["matches"][selected]].mean()))
        false_match.append(float(accepted[selected][~test["matches"][selected]].mean()))
    return {"threshold": threshold, "validation_fmr": float(np.mean(validation["scores"][~validation["matches"]] >= threshold)),
            "tar": float(np.mean(true_accept)), "fmr": float(np.mean(false_match)),
            "genuine_pairs": int(test["matches"].sum()), "impostor_pairs": int((~test["matches"]).sum()),
            "identity_tar": true_accept, "identity_fmr": false_match,
            "identities": test["identities"]}


def summarise(records: list[dict]) -> list[dict]:
    rows = []
    for dataset in DATASETS:
        baseline = sorted([record for record in records if record["dataset"] == dataset and record["policy"] == "recurring"],
                          key=lambda record: record["master_seed"])
        for policy in ["separated", "partial"]:
            candidate = sorted([record for record in records if record["dataset"] == dataset and record["policy"] == policy],
                               key=lambda record: record["master_seed"])
            if len(baseline) != 3 or len(candidate) != 3:
                raise ValueError("Full three-seed pairs required")
            identities = sorted(baseline[0]["attack"]["identity_top1_scores"])
            for record in baseline + candidate:
                if sorted(record["attack"]["identity_top1_scores"]) != identities or record["utility"]["identities"] != identities:
                    raise ValueError("Attack and verification identity ordering differ")
            before_leakage = np.asarray([[record["attack"]["identity_top1_scores"][identity] for identity in identities] for record in baseline])
            after_leakage = np.asarray([[record["attack"]["identity_top1_scores"][identity] for identity in identities] for record in candidate])
            before_tar = np.asarray([record["utility"]["identity_tar"] for record in baseline])
            after_tar = np.asarray([record["utility"]["identity_tar"] for record in candidate])
            after_fmr = np.asarray([record["utility"]["identity_fmr"] for record in candidate])
            alpha = .05 / 6 if policy == "separated" else .05
            leakage_lower, leakage_upper = paired_mean_interval(before_leakage - after_leakage, 92641, 10000, alpha)
            tar_lower, tar_upper = paired_mean_interval(after_tar - before_tar, 92641, 10000, alpha)
            _, fmr_upper = paired_mean_interval(after_fmr, 92641, 10000, alpha)
            rows.append({"dataset": dataset, "candidate": policy, "primary": policy == "separated",
                         "before_leakage": float(before_leakage.mean()), "after_leakage": float(after_leakage.mean()),
                         "leakage_reduction_lower": leakage_lower, "leakage_reduction_upper": leakage_upper,
                         "before_tar": float(before_tar.mean()), "after_tar": float(after_tar.mean()),
                         "tar_difference_lower": tar_lower, "tar_difference_upper": tar_upper,
                         "before_fmr": float(np.mean([record["utility"]["fmr"] for record in baseline])),
                         "after_fmr": float(after_fmr.mean()), "after_fmr_upper": fmr_upper,
                         "utility_margin": .03, "fmr_limit": .02, "tail_alpha": alpha,
                         "gate_pass": acceptance_gate(leakage_lower, tar_lower, fmr_upper, .03, .02),
                         "chance": 1 / len(identities)})
    return rows


def execute() -> dict:
    if STUDY.exists() or PRIVATE.exists():
        raise FileExistsError("Frozen outputs exist; do not overwrite them")
    source_paths = sorted(set(list((ROOT / "src/biometrics_ai").rglob("*.py")) +
                              list((ROOT / "scripts/train").glob("*.py")) +
                              [ROOT / "scripts/diagnostics/source_policy_recipes.py",
                               ROOT / "scripts/diagnostics/benchmark_source_analysis.py",
                               ROOT / "docs/protocols/source_security_utility_2026-09-25.md",
                               ROOT / "docs/theory/source_scope_and_utility.md"]))
    input_paths = [ROOT / directory / name for directory in DATASETS.values()
                   for name in ["embeddings.npy", "metadata.json", "embedding_manifest.json"]]
    manifest = {"status": "running", "started_utc": datetime.now(timezone.utc).isoformat(),
                "source_sha256": {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in source_paths},
                "input_sha256": {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in input_paths},
                "software": {name: version(name) for name in ["numpy", "torch", "scipy", "scikit-learn", "bandit", "threadpoolctl"]},
                "base_commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip(),
                "dirty_worktree": True, "budget_seconds": 3600, "torch_threads": 8, "blas_threads": 1,
                "master_seeds": MASTER_SEEDS, "model_seeds": MODEL_SEEDS, "training": TRAINING,
                "split_seed": 92583, "set_seed": 92627, "template_dim": 64, "shared_dimensions": 16,
                "independent_review": "pending; same-author fixtures with separate runtime oracle"}
    STUDY.mkdir(parents=True)
    PRIVATE.mkdir(parents=True)
    manifest_path = STUDY / "execution_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    started = time.monotonic()
    deadline = started + 3600
    records, exported = [], []
    try:
        source = (ROOT / "scripts/diagnostics/source_policy_recipes.py").read_text()
        audits = {policy: analyse_source(source, policy) for policy in POLICIES}
        if [audits[policy]["decision"] for policy in POLICIES] != ["reuse", "reuse", "conditional_fresh"]:
            raise RuntimeError("Executable recipe source audit does not match planned study")
        (STUDY / "source_audits.json").write_text(json.dumps(audits, indent=2) + "\n")
        manifest["benchmark"] = benchmark(STUDY / "benchmark")
        torch.set_num_threads(8)
        with threadpool_limits(limits=1, user_api="blas"):
            for dataset, directory in DATASETS.items():
                embeddings, metadata, _ = runner.load_embeddings(ROOT / directory)
                if not np.isfinite(embeddings).all() or not np.allclose(np.linalg.norm(embeddings, axis=1), 1, atol=1e-4):
                    raise ValueError("Finite unit embeddings are required")
                metadata = runner.reassign_identity_splits(metadata, 92583)
                for master, model_seed in zip(MASTER_SEEDS, MODEL_SEEDS):
                    for policy in POLICIES:
                        print(f"Starting {dataset} / {policy} / key {master}", flush=True)
                        templates = protect(embeddings, policy, master, deadline)
                        sets = {split: build_real_exposure_sets(embeddings, templates, metadata, split,
                                                               ExposureSetConfig(10, 8, 92627))
                                for split in ["train", "val", "test"]}
                        attack = runner.train_model("mean_mlp", sets["train"], sets["val"], sets["test"],
                                                    {**TRAINING, "deadline_monotonic": deadline}, model_seed)
                        legitimate = utility(embeddings, metadata, policy, master, deadline)
                        record = {"dataset": dataset, "policy": policy, "master_seed": master,
                                  "model_seed": model_seed, "attack": attack, "utility": legitimate}
                        records.append(record)
                        (PRIVATE / f"{dataset}_{policy}_{master}.json").write_text(json.dumps(record, indent=2) + "\n")
                        exported.append({"dataset": dataset, "policy": policy, "master_seed": master,
                                         "model_seed": model_seed, "attacker_top1": attack["top1_linkage"],
                                         "best_epoch": attack["best_epoch"],
                                         **{key: value for key, value in legitimate.items() if key not in {"identity_tar", "identity_fmr", "identities"}}})
                        write_table(STUDY / "endpoints.csv", exported)
                        print(f"  attacker={attack['top1_linkage']:.4f}, TAR={legitimate['tar']:.4f}, FMR={legitimate['fmr']:.4f}", flush=True)
        effects = summarise(records)
        write_table(STUDY / "security_utility_effects.csv", effects)
        manifest["status"] = "completed"
        manifest["trained_endpoints"] = len(records)
        manifest["primary_gate_passes"] = sum(row["primary"] and row["gate_pass"] for row in effects)
    except Exception:
        manifest["status"] = "failed"
        manifest["trained_endpoints"] = len(records)
        raise
    finally:
        manifest["wall_seconds"] = time.monotonic() - started
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


if __name__ == "__main__":
    result = execute()
    print(json.dumps({key: result[key] for key in ["status", "trained_endpoints", "primary_gate_passes", "wall_seconds"]}, indent=2))