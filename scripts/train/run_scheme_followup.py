"""Execute and analyse a hash-frozen, bounded scheme follow-up."""
from __future__ import annotations

import argparse
import copy
from datetime import datetime, timezone
import hashlib
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

from scripts.train import run_real_multiexposure as runner
from scripts.train.run_scheme_extension_pilot import run_pilots, write_table


def holm_adjust(values: list[float], family_size: int) -> list[float]:
    probabilities = np.asarray(values, dtype=float)
    if family_size < len(probabilities) or not np.isfinite(probabilities).all() or np.any((probabilities < 0) | (probabilities > 1)):
        raise ValueError("Invalid p-values or planned family size")
    order = np.argsort(probabilities)
    adjusted = np.empty(len(probabilities))
    adjusted[order] = np.minimum(1, np.maximum.accumulate(probabilities[order] * (family_size - np.arange(len(probabilities)))))
    return adjusted.tolist()


def crossed_interval(scores: np.ndarray, seed: int, resamples: int) -> tuple[float, float]:
    scores = np.asarray(scores, dtype=float)
    if scores.ndim != 2 or min(scores.shape) < 2 or not np.isfinite(scores).all() or resamples < 1:
        raise ValueError("Expected finite model-seed by identity scores")
    rng = np.random.default_rng(seed)
    seeds = rng.integers(scores.shape[0], size=(resamples, scores.shape[0]))
    identities = rng.integers(scores.shape[1], size=(resamples, scores.shape[1]))
    estimates = scores[seeds[:, :, None], identities[:, None, :]].mean(axis=(1, 2))
    return tuple(float(value) for value in np.quantile(estimates, [0.025, 0.975]))


def native_null_test(confusion: np.ndarray, seed: int, permutations: int) -> tuple[float, float, np.ndarray]:
    confusion = np.asarray(confusion, dtype=float)
    if confusion.ndim != 2 or confusion.shape[0] != confusion.shape[1] or len(confusion) < 2:
        raise ValueError("Expected square identity confusion matrix")
    if not np.isfinite(confusion).all() or np.any(confusion < 0) or not np.allclose(confusion.sum(axis=1), 1):
        raise ValueError("Each identity row must be a probability distribution")
    if permutations < 1:
        raise ValueError("Positive permutation count required")
    rng = np.random.default_rng(seed)
    observed = float(np.diag(confusion).mean())
    null = np.asarray([confusion[np.arange(len(confusion)), rng.permutation(len(confusion))].mean()
                       for _ in range(permutations)])
    probability = float((1 + (null >= observed - 1e-12).sum()) / (permutations + 1))
    return observed, probability, null


def run_controls(config: dict, deadline: float) -> None:
    analysis = config["analysis"]
    native_rows, norm_rows = [], []
    scheme = next(item for item in config["schemes"] if item["name"] == "PolyProtect")
    for dataset in config["datasets"]:
        if time.monotonic() >= deadline:
            raise TimeoutError("Control budget exhausted")
        embeddings, metadata, _ = runner.load_embeddings(Path(dataset["embedding_dir"]))
        metadata = runner.reassign_identity_splits(metadata, dataset["split_reassignment_seed"])
        indices = [index for index, record in enumerate(metadata) if record["split"] == "test"]
        values = embeddings[indices]
        records = [metadata[index] for index in indices]
        identity_ids = sorted({str(record["identity_id"]) for record in records})
        gallery_indices, probe_indices, probe_labels = [], [], []
        for label, identity in enumerate(identity_ids):
            members = sorted([index for index, record in enumerate(records) if str(record["identity_id"]) == identity],
                             key=lambda index: int(records[index]["sample_index"]))
            gallery_indices.append(members[0])
            probe_indices.extend(members[1:])
            probe_labels.extend([label] * (len(members) - 1))
        probe_labels = np.asarray(probe_labels)
        for key_seed in analysis["native_key_seeds"]:
            if time.monotonic() >= deadline:
                raise TimeoutError("Control budget exhausted")
            templates, _ = runner.protect_embeddings(values, records, "independent_unseen_keys", key_seed,
                                                     scheme["template_dim"], scheme["protection"])
            normalized = templates.astype(float)
            normalized /= np.linalg.norm(normalized, axis=1, keepdims=True).clip(min=1e-12)
            predictions = np.argsort(-(normalized[probe_indices] @ normalized[gallery_indices].T), axis=1)[:, 0]
            confusion = np.stack([np.bincount(predictions[probe_labels == label], minlength=len(identity_ids)) /
                                  (probe_labels == label).sum() for label in range(len(identity_ids))])
            observed, probability, null = native_null_test(confusion, analysis["seed"], analysis["permutations"])
            identity_scores = np.diag(confusion)
            rng = np.random.default_rng(analysis["seed"])
            draws = identity_scores[rng.integers(len(identity_ids), size=(analysis["bootstrap_resamples"], len(identity_ids)))].mean(axis=1)
            native_rows.append({"dataset": dataset["name"], "split_seed": dataset["split_reassignment_seed"],
                                "key_seed": key_seed, "scheme": "PolyProtect", "chance": 1 / len(identity_ids),
                                "identity_balanced_top1": observed, "probe_weighted_top1": float((predictions == probe_labels).mean()),
                                "lower95": float(np.quantile(draws, 0.025)), "upper95": float(np.quantile(draws, 0.975)),
                                "permutation_p": probability, "null_mean": float(null.mean()),
                                "identity_clusters": len(identity_ids), "permutations": analysis["permutations"]})
        sample_count = min(analysis["norm_probe_count"], len(values))
        for protection in config["schemes"]:
            if time.monotonic() >= deadline:
                raise TimeoutError("Control budget exhausted")
            original, _ = runner.protect_embeddings(values[:sample_count], records[:sample_count], "independent_unseen_keys",
                                                     analysis["native_key_seeds"][0], protection["template_dim"], protection["protection"])
            for scale in analysis["norm_scales"]:
                scaled, _ = runner.protect_embeddings(values[:sample_count] * scale, records[:sample_count], "independent_unseen_keys",
                                                       analysis["native_key_seeds"][0], protection["template_dim"], protection["protection"])
                original_norm = np.linalg.norm(original, axis=1)
                scaled_norm = np.linalg.norm(scaled, axis=1)
                cosines = np.sum(original * scaled, axis=1) / np.maximum(original_norm * scaled_norm, 1e-12)
                norm_rows.append({"dataset": dataset["name"], "split_seed": dataset["split_reassignment_seed"],
                                  "scheme": protection["name"], "scale": scale, "sample_count": sample_count,
                                  "relative_l2_mean": float(np.mean(np.linalg.norm(scaled - original, axis=1) / np.maximum(original_norm, 1e-12))),
                                  "cosine_mean": float(cosines.mean()), "exactly_equal": bool(np.array_equal(original, scaled)),
                                  "interpretation": "synthetic radial stress; not natural norm leakage"})
        print(f"Controls complete: {dataset['name']} / split {dataset['split_reassignment_seed']}", flush=True)
    corrected = holm_adjust([row["permutation_p"] for row in native_rows], len(config["datasets"]) * len(analysis["native_key_seeds"]))
    for row, probability in zip(native_rows, corrected):
        row["holm_p"] = probability
    destination = Path(config["summary_dir"])
    write_table(destination / "native_null_controls.csv", native_rows)
    write_table(destination / "norm_sensitivity.csv", norm_rows)


def analyse_runs(config: dict) -> None:
    analysis = config["analysis"]
    endpoints, contrasts = [], []
    for path in sorted(Path(config["output_root"]).rglob("metrics.json")):
        result = json.loads(path.read_text())
        cell = yaml.safe_load((path.parent / "run_config.yaml").read_text())
        common = {"stage": result["stage"], "dataset": result["dataset"], "scheme": cell["scheme_label"],
                  "split_seed": result["split_reassignment_seed"], "chance": 1 / result["split_identity_counts"]["test"]}
        for condition, condition_result in result["conditions"].items():
            reference = condition_result["exposures"]["1"]["models"]["single_mlp"]["runs"]
            identities = sorted(reference[0]["identity_top1_scores"])
            reference_by_seed = {run["seed"]: run["identity_top1_scores"] for run in reference}
            for exposure, exposure_result in condition_result["exposures"].items():
                for model, model_result in exposure_result["models"].items():
                    runs = sorted(model_result["runs"], key=lambda item: item["seed"])
                    if any(set(run["identity_top1_scores"]) != set(identities) for run in runs):
                        raise ValueError("Endpoint identities do not align")
                    scores = np.asarray([[run["identity_top1_scores"][identity] for identity in identities] for run in runs])
                    lower, upper = crossed_interval(scores, analysis["seed"], analysis["bootstrap_resamples"])
                    endpoint = {**common, "condition": condition, "exposures": int(exposure), "model": model,
                                "model_seeds": len(runs), "identity_clusters": len(identities), "top1_mean": float(scores.mean()),
                                "seed_sd": float(scores.mean(axis=1).std(ddof=1)), "lower95": lower, "upper95": upper}
                    endpoints.append(endpoint)
                    if int(exposure) != 10:
                        continue
                    before = np.asarray([[reference_by_seed[run["seed"]][identity] for identity in identities] for run in runs])
                    difference = scores - before
                    lower, upper = crossed_interval(difference, analysis["seed"], analysis["bootstrap_resamples"])
                    primary = condition == "random_key_pool_4" and model == "mean_mlp"
                    probability = float(permutation_test((difference.mean(axis=0),), np.mean, permutation_type="samples",
                                                        vectorized=True, alternative="greater", n_resamples=analysis["permutations"],
                                                        rng=np.random.default_rng(analysis["seed"])).pvalue) if primary else None
                    contrasts.append({**common, "condition": condition, "model": model, "model_seeds": len(runs),
                                      "identity_clusters": len(identities), "gain": float(difference.mean()),
                                      "seed_sd": float(difference.mean(axis=1).std(ddof=1)), "lower95": lower, "upper95": upper,
                                      "primary": primary, "signflip_p": probability, "holm_p": None})
    primary_rows = [row for row in contrasts if row["primary"]]
    for row, probability in zip(primary_rows, holm_adjust([row["signflip_p"] for row in primary_rows], analysis["primary_family_size"])):
        row["holm_p"] = probability
    destination = Path(config["summary_dir"])
    write_table(destination / "seed_identity_endpoints.csv", endpoints)
    write_table(destination / "seed_identity_contrasts.csv", contrasts)


def execute(config_path: Path) -> None:
    config = yaml.safe_load(config_path.read_text())
    if config["stage"] != "bounded_validation" or not 0 < config["max_wall_seconds"] <= 3600:
        raise ValueError("Only authorized bounded validation is supported")
    destination = Path(config["summary_dir"])
    destination.mkdir(parents=True, exist_ok=True)
    manifest_path = destination / "execution_manifest.json"
    if manifest_path.exists():
        raise FileExistsError("Execution already frozen; use --analyse-only for saved results")
    protocol_doc = ROOT / f"docs/protocols/{config_path.stem}.md"
    sources = sorted(set([config_path.resolve(), protocol_doc] +
                         list((ROOT / "src/biometrics_ai").rglob("*.py")) + list((ROOT / "scripts/train").glob("*.py"))))
    hashes = {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    manifest = {"started_utc": datetime.now(timezone.utc).isoformat(),
                "base_commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip(),
                "dirty_worktree": bool(subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True).stdout.strip()),
                "source_sha256": hashes, "budget_seconds": config["max_wall_seconds"], "torch_threads": 8,
                "freeze_method": "pre-execution source/config hashes; not a new Git commit"}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    torch.set_num_threads(8)
    started = time.monotonic()
    deadline = started + config["max_wall_seconds"]
    try:
        run_controls(config, min(deadline, started + 480))
        training_config = copy.deepcopy(config)
        training_config["max_wall_seconds"] = min(3000, max(0, deadline - time.monotonic() - 60))
        if training_config["max_wall_seconds"] <= 0:
            raise TimeoutError("No training budget remains")
        status = run_pilots(training_config)
        analyse_runs(config)
        manifest["status"] = "completed" if status["all_cells_complete"] else "partial"
        print(json.dumps({key: value for key, value in status.items() if key != "cells"}, indent=2))
    except Exception:
        manifest["status"] = "failed"
        raise
    finally:
        manifest["wall_seconds"] = time.monotonic() - started
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs/attacks/scheme_followup_2026-09-18.yaml")
    parser.add_argument("--analyse-only", action="store_true")
    args = parser.parse_args()
    if args.analyse_only:
        analyse_runs(yaml.safe_load(args.config.read_text()))
    else:
        execute(args.config)


if __name__ == "__main__":
    main()