"""Run a Month 1 single-template real-data engineering experiment."""
from __future__ import annotations

import argparse
import copy
import csv
import json
import subprocess
import sys
import time
from collections import defaultdict
from importlib.metadata import version
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import numpy as np
import torch
import yaml
from torch.nn import functional as F

from biometrics_ai.aggregation.models import SingleTemplateMLP
from biometrics_ai.evaluation.metrics import gallery_probe_metrics, verification_metrics
from biometrics_ai.protection import BioHashConfig, biohash, biohash_batch, generate_key
from biometrics_ai.utils.seeding import seed_record_dict


def load_embeddings(directory: Path) -> tuple[np.ndarray, list[dict], dict]:
    embeddings = np.load(directory / "embeddings.npy").astype(np.float32)
    metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
    manifest = json.loads((directory / "embedding_manifest.json").read_text(encoding="utf-8"))
    if len(embeddings) != len(metadata):
        raise ValueError("Embedding and metadata counts differ")
    if embeddings.ndim != 2 or embeddings.shape[1] != 512:
        raise ValueError(f"Expected 512-D ArcFace embeddings, got {embeddings.shape}")
    if not np.all(np.isfinite(embeddings)):
        raise ValueError("Embeddings contain non-finite values")
    norms = np.linalg.norm(embeddings, axis=1)
    if not np.allclose(norms, 1.0, atol=1e-5):
        raise ValueError("Embeddings are not L2-normalized")
    return embeddings, metadata, manifest


def validate_splits(metadata: list[dict]) -> dict[str, set[str]]:
    split_identities = {
        split: {str(row["identity_id"]) for row in metadata if row["split"] == split}
        for split in ("train", "val", "test")
    }
    if split_identities["train"] & (split_identities["val"] | split_identities["test"]):
        raise ValueError("Training identities overlap validation or test identities")
    if split_identities["val"] & split_identities["test"]:
        raise ValueError("Validation and test identities overlap")
    if not all(split_identities.values()):
        raise ValueError("Every split must contain identities")
    return split_identities


def gallery_probe_indices(metadata: list[dict]) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for index, row in enumerate(metadata):
        if row["split"] == "test":
            grouped[str(row["identity_id"])].append(index)
    gallery_indices, gallery_ids, probe_indices, probe_ids = [], [], [], []
    for identity_id in sorted(grouped):
        indices = sorted(grouped[identity_id], key=lambda index: int(metadata[index]["sample_index"]))
        if len(indices) < 2:
            continue
        gallery_indices.append(indices[0])
        gallery_ids.append(identity_id)
        probe_indices.extend(indices[1:])
        probe_ids.extend([identity_id] * (len(indices) - 1))
    if len(gallery_indices) < 2:
        raise ValueError("At least two test identities with gallery and probe samples are required")
    return (
        np.asarray(gallery_indices),
        np.asarray(gallery_ids),
        np.asarray(probe_indices),
        np.asarray(probe_ids),
    )


def score_matrix_metrics(scores: np.ndarray, probe_ids: np.ndarray, gallery_ids: np.ndarray) -> dict[str, float]:
    matches = probe_ids[:, None] == gallery_ids[None, :]
    genuine_scores = scores[matches]
    impostor_scores = scores[~matches]
    ranking = np.argsort(-scores, axis=1)
    ranked_ids = gallery_ids[ranking]
    top5_width = min(5, len(gallery_ids))
    return {
        "mean_genuine_similarity": float(genuine_scores.mean()),
        "mean_impostor_similarity": float(impostor_scores.mean()),
        "top1_linkage": float(np.mean(ranked_ids[:, 0] == probe_ids)),
        "top5_linkage": float(np.mean(np.any(ranked_ids[:, :top5_width] == probe_ids[:, None], axis=1))),
        **verification_metrics(genuine_scores, impostor_scores),
    }


def protect_embeddings(
    embeddings: np.ndarray,
    metadata: list[dict],
    condition: str,
    key_seed: int,
    template_dim: int,
) -> tuple[np.ndarray, dict[str, int | bool]]:
    scheme = BioHashConfig(input_dim=embeddings.shape[1], output_dim=template_dim)
    if condition == "shared_key_calibration":
        key = generate_key(key_seed, "shared", 0)
        return biohash_batch(embeddings, key, scheme).astype(np.float32), {
            "unique_keys": 1,
            "split_key_disjoint": False,
        }
    if condition != "independent_unseen_keys":
        raise ValueError(f"Unknown condition: {condition}")

    templates, keys_by_split = [], defaultdict(set)
    for index, (embedding, row) in enumerate(zip(embeddings, metadata, strict=True)):
        split = str(row["split"])
        key = generate_key(key_seed, split, index)
        templates.append(biohash(embedding, key, scheme))
        keys_by_split[split].add(key)
    split_key_disjoint = not (
        keys_by_split["train"] & keys_by_split["val"]
        or keys_by_split["train"] & keys_by_split["test"]
        or keys_by_split["val"] & keys_by_split["test"]
    )
    unique_key_count = sum(len(values) for values in keys_by_split.values())
    if unique_key_count != len(metadata):
        raise RuntimeError("Independent key generation produced duplicate keys within a split")
    if not split_key_disjoint:
        raise RuntimeError("Independent key generation produced overlapping split key pools")
    return np.asarray(templates, dtype=np.float32), {
        "unique_keys": unique_key_count,
        "split_key_disjoint": split_key_disjoint,
    }


def train_attacker(
    templates: np.ndarray,
    embeddings: np.ndarray,
    metadata: list[dict],
    gallery_indices: np.ndarray,
    gallery_ids: np.ndarray,
    probe_indices: np.ndarray,
    probe_ids: np.ndarray,
    training_config: dict,
    seed: int,
) -> dict[str, float | int | dict]:
    started = time.time()
    seed_record = seed_record_dict(seed)
    train_indices = np.asarray([index for index, row in enumerate(metadata) if row["split"] == "train"])
    validation_indices = np.asarray([index for index, row in enumerate(metadata) if row["split"] == "val"])
    train_inputs = torch.tensor(templates[train_indices], dtype=torch.float32)
    train_targets = torch.tensor(embeddings[train_indices], dtype=torch.float32)
    validation_inputs = torch.tensor(templates[validation_indices], dtype=torch.float32)
    validation_targets = torch.tensor(embeddings[validation_indices], dtype=torch.float32)

    model = SingleTemplateMLP(
        templates.shape[1],
        embeddings.shape[1],
        hidden_dim=int(training_config["hidden_dim"]),
    )
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=float(training_config["learning_rate"]),
        weight_decay=float(training_config["weight_decay"]),
    )
    best_state = copy.deepcopy(model.state_dict())
    best_validation_loss = float("inf")
    best_epoch = 0
    stale_epochs = 0
    for epoch in range(1, int(training_config["epochs"]) + 1):
        model.train()
        optimizer.zero_grad()
        predictions = model(train_inputs)
        training_loss = (1 - F.cosine_similarity(predictions, train_targets, dim=-1)).mean()
        training_loss = training_loss + float(training_config["mse_weight"]) * F.mse_loss(predictions, train_targets)
        training_loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            validation_predictions = model(validation_inputs)
            validation_loss = (1 - F.cosine_similarity(validation_predictions, validation_targets, dim=-1)).mean()
            validation_loss = validation_loss + float(training_config["mse_weight"]) * F.mse_loss(
                validation_predictions, validation_targets
            )
        if float(validation_loss) < best_validation_loss - 1e-6:
            best_validation_loss = float(validation_loss)
            best_epoch = epoch
            best_state = copy.deepcopy(model.state_dict())
            stale_epochs = 0
        else:
            stale_epochs += 1
            if stale_epochs >= int(training_config["patience"]):
                break

    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        probe_predictions = model(torch.tensor(templates[probe_indices], dtype=torch.float32)).numpy()
    target_cosines = np.sum(probe_predictions * embeddings[probe_indices], axis=1)
    metrics: dict[str, float | int | dict] = {
        "seed": seed,
        "seed_record": seed_record,
        "best_epoch": best_epoch,
        "best_validation_loss": best_validation_loss,
        "mean_target_cosine": float(target_cosines.mean()),
        "normalized_l2": float(np.linalg.norm(probe_predictions - embeddings[probe_indices], axis=1).mean()),
        "elapsed_seconds": time.time() - started,
        **gallery_probe_metrics(probe_predictions, embeddings[gallery_indices], probe_ids, gallery_ids),
    }
    return metrics


def aggregate_runs(runs: list[dict]) -> dict[str, dict[str, float]]:
    metric_names = (
        "mean_target_cosine",
        "normalized_l2",
        "mean_genuine_cosine",
        "mean_impostor_cosine",
        "top1_linkage",
        "top5_linkage",
        "auroc",
        "eer",
        "tar_at_far_1e-2",
        "tar_at_far_1e-3",
    )
    summary = {}
    for metric_name in metric_names:
        values = np.asarray([float(run[metric_name]) for run in runs])
        summary[metric_name] = {
            "mean": float(values.mean()),
            "std": float(values.std(ddof=1)) if len(values) > 1 else 0.0,
        }
    return summary


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    if config.get("classification") != "engineering validation, not benchmark_cb reproduction":
        raise ValueError("Month 1 runs must retain the engineering-validation classification")
    dataset = str(config.get("dataset", "")).strip()
    if not dataset:
        raise ValueError("Month 1 runs must name the dataset in the experiment config")

    embeddings, metadata, embedding_manifest = load_embeddings(Path(config["embedding_dir"]))
    split_identities = validate_splits(metadata)
    gallery_indices, gallery_ids, probe_indices, probe_ids = gallery_probe_indices(metadata)
    unprotected_baseline = gallery_probe_metrics(
        embeddings[probe_indices], embeddings[gallery_indices], probe_ids, gallery_ids
    )

    condition_results = {}
    for condition in config["conditions"]:
        templates, key_audit = protect_embeddings(
            embeddings,
            metadata,
            condition,
            int(config["key_seed"]),
            int(config["template_dim"]),
        )
        protected_scores = 1.0 - np.mean(
            templates[probe_indices, None, :] != templates[gallery_indices][None, :, :],
            axis=2,
        )
        protected_baseline = score_matrix_metrics(protected_scores, probe_ids, gallery_ids)
        runs = [
            train_attacker(
                templates,
                embeddings,
                metadata,
                gallery_indices,
                gallery_ids,
                probe_indices,
                probe_ids,
                config["training"],
                int(seed),
            )
            for seed in config["training"]["seeds"]
        ]
        condition_results[condition] = {
            "key_audit": key_audit,
            "protected_template_baseline": protected_baseline,
            "attacker_runs": runs,
            "attacker_summary": aggregate_runs(runs),
        }

    result = {
        "classification": config["classification"],
        "dataset": dataset,
        "embedding_manifest": embedding_manifest,
        "sample_count": len(metadata),
        "split_identity_counts": {key: len(value) for key, value in split_identities.items()},
        "gallery_identities": len(gallery_ids),
        "probe_samples": len(probe_ids),
        "chance_top1": 1.0 / len(gallery_ids),
        "unprotected_arcface_baseline": unprotected_baseline,
        "conditions": condition_results,
        "software": {
            "numpy": version("numpy"),
            "torch": version("torch"),
            "scikit-learn": version("scikit-learn"),
        },
        "git_commit": subprocess.run(["git", "rev-parse", "HEAD"], text=True, capture_output=True).stdout.strip(),
    }

    results_directory = Path(config["results_dir"])
    results_directory.mkdir(parents=True, exist_ok=True)
    (results_directory / "run_config.yaml").write_text(yaml.safe_dump(config, sort_keys=True), encoding="utf-8")
    (results_directory / "metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    with (results_directory / "summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["condition", "metric", "mean", "std"])
        for condition, values in condition_results.items():
            for metric_name, statistics in values["attacker_summary"].items():
                writer.writerow([condition, metric_name, statistics["mean"], statistics["std"]])
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()