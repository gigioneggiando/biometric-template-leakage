"""Run the preregistered real-data multi-exposure protected-template study."""
from __future__ import annotations

import argparse
import copy
import csv
import json
import subprocess
import sys
import time
from importlib.metadata import version
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))

import numpy as np
import torch
import yaml
from torch.nn import functional as F

from biometrics_ai.aggregation.models import DeepSetsExtractor, PooledTemplateMLP, SingleTemplateMLP
from biometrics_ai.data.multiexposure import ExposureSetConfig, build_real_exposure_sets, shuffle_non_anchor_records
from biometrics_ai.evaluation.metrics import gallery_probe_metrics, identity_clustered_top1_interval
from biometrics_ai.protection import (
    BioHashConfig,
    MLPHashConfig,
    biohash,
    biohash_batch,
    correlated_biohash,
    generate_key,
    mlphash,
    mlphash_batch,
)
from biometrics_ai.utils.seeding import seed_record_dict


def load_embeddings(directory: Path) -> tuple[np.ndarray, list[dict], dict]:
    embeddings = np.load(directory / "embeddings.npy").astype(np.float32)
    metadata = json.loads((directory / "metadata.json").read_text(encoding="utf-8"))
    manifest = json.loads((directory / "embedding_manifest.json").read_text(encoding="utf-8"))
    if len(embeddings) != len(metadata):
        raise ValueError("Embedding and metadata counts differ")
    if embeddings.ndim != 2 or embeddings.shape[1] != 512:
        raise ValueError(f"Expected 512-D embeddings, got {embeddings.shape}")
    split_ids = {
        split: {str(row["identity_id"]) for row in metadata if row["split"] == split}
        for split in ("train", "val", "test")
    }
    if not all(split_ids.values()) or split_ids["train"] & split_ids["val"] or split_ids["train"] & split_ids["test"] or split_ids["val"] & split_ids["test"]:
        raise ValueError("Embedding metadata must contain non-empty identity-disjoint splits")
    return embeddings, metadata, manifest


def reassign_identity_splits(metadata: list[dict], seed: int) -> list[dict]:
    """Permute identities across splits while preserving per-split identity counts."""
    identity_split = {}
    for row in metadata:
        identity_split.setdefault(str(row["identity_id"]), row["split"])
    identities = sorted(identity_split)
    ordered_splits = [identity_split[identity] for identity in identities]
    permuted = np.random.default_rng(generate_key(seed, "split_reassignment", 0)).permutation(len(identities))
    new_split = {identities[source]: ordered_splits[position] for position, source in enumerate(permuted)}
    reassigned = copy.deepcopy(metadata)
    for row in reassigned:
        row["split"] = new_split[str(row["identity_id"])]
    return reassigned


def protect_embeddings(
    embeddings: np.ndarray,
    metadata: list[dict],
    condition: str,
    key_seed: int,
    template_dim: int,
    protection: dict | None = None,
) -> tuple[np.ndarray, dict]:
    protection = protection or {"scheme": "biohash"}
    scheme_name = str(protection["scheme"])
    if scheme_name == "biohash":
        scheme = BioHashConfig(
            input_dim=embeddings.shape[1],
            output_dim=template_dim,
            haar_sign_corrected=bool(protection.get("haar_sign_corrected", False)),
        )
        protect_one, protect_batch = biohash, biohash_batch
    elif scheme_name == "mlphash_paper_specified":
        scheme = MLPHashConfig(
            input_dim=embeddings.shape[1],
            output_dim=template_dim,
            hidden_dim=int(protection.get("hidden_dim", embeddings.shape[1] * 2)),
            hidden_layers=int(protection.get("hidden_layers", 3)),
        )
        protect_one, protect_batch = mlphash, mlphash_batch
    else:
        raise ValueError(f"Unknown protection scheme: {scheme_name}")
    if condition == "shared_key_calibration":
        key = generate_key(key_seed, "shared", 0)
        templates = protect_batch(embeddings, key, scheme)
        return templates, {"scheme": scheme_name, "unique_keys": 1, "split_key_disjoint": False}
    if condition.startswith("correlated_key_"):
        if scheme_name != "biohash":
            raise ValueError("Correlated-key controls currently support BioHash only")
        shared_percent = int(condition.removeprefix("correlated_key_"))
        if shared_percent not in {0, 25, 50, 75, 100}:
            raise ValueError("Correlated-key percentage must be one of 0, 25, 50, 75, or 100")
        shared_dimensions = template_dim * shared_percent // 100
        shared_key = generate_key(key_seed, "correlated_shared_projection", 0)
        private_keys = [
            generate_key(key_seed, str(row["split"]), f"correlated:{row['sample_id']}")
            for row in metadata
        ]
        templates = np.stack(
            [
                correlated_biohash(embedding, shared_key, private_key, shared_dimensions, scheme)
                for embedding, private_key in zip(embeddings, private_keys)
            ]
        )
        return templates, {
            "scheme": scheme_name,
            "private_keys": len(set(private_keys)),
            "split_private_keys_disjoint": True,
            "shared_projection_dimensions": shared_dimensions,
            "shared_projection_fraction": shared_percent / 100,
            "key_scope": "partially correlated per-record keys",
        }
    if condition.startswith(("system_key_pool_", "random_key_pool_")):
        random_assignment = condition.startswith("random_key_pool_")
        prefix = "random_key_pool_" if random_assignment else "system_key_pool_"
        key_pool_size = int(condition.removeprefix(prefix))
        if key_pool_size < 1:
            raise ValueError("System key pool size must be positive")
        key_pool = [generate_key(key_seed, "system_pool", index) for index in range(key_pool_size)]
        if random_assignment:
            key_slots = [
                generate_key(key_seed, "pool_assignment", str(row["sample_id"])) % key_pool_size
                for row in metadata
            ]
        else:
            key_slots = [int(row["sample_index"]) % key_pool_size for row in metadata]
        keys = [key_pool[slot] for slot in key_slots]
        templates = np.stack([protect_one(embedding, key, scheme) for embedding, key in zip(embeddings, keys)])
        slot_known = bool(protection.get("include_key_slot", False))
        if slot_known:
            templates = np.concatenate(
                [templates.astype(np.float32), np.eye(key_pool_size, dtype=np.float32)[key_slots]],
                axis=1,
            )
        audit = {
            "scheme": scheme_name,
            "unique_keys": len(set(keys)),
            "split_key_disjoint": False,
            "key_scope": "system-wide recurring randomized" if random_assignment else "system-wide recurring",
            "key_pool_size": key_pool_size,
        }
        if slot_known:
            audit["attacker_key_slot_known"] = True
        return templates, audit
    if protection.get("include_key_slot", False):
        raise ValueError("include_key_slot is valid only for recurring key-pool conditions")
    if condition != "independent_unseen_keys":
        raise ValueError(f"Unknown condition: {condition}")

    keys = [generate_key(key_seed, str(row["split"]), str(row["sample_id"])) for row in metadata]
    if len(set(keys)) != len(keys):
        raise RuntimeError("Independent key generation produced duplicate keys")
    split_keys = {
        split: {key for key, row in zip(keys, metadata) if row["split"] == split}
        for split in ("train", "val", "test")
    }
    if split_keys["train"] & split_keys["val"] or split_keys["train"] & split_keys["test"] or split_keys["val"] & split_keys["test"]:
        raise RuntimeError("Independent key generation produced overlapping split key pools")
    templates = np.stack([protect_one(embedding, key, scheme) for embedding, key in zip(embeddings, keys)])
    return templates, {"scheme": scheme_name, "unique_keys": len(keys), "split_key_disjoint": True}


def build_same_image_different_key_sets(
    embeddings: np.ndarray,
    metadata: list[dict],
    split: str,
    set_config: ExposureSetConfig,
    key_seed: int,
    template_dim: int,
    protection: dict | None = None,
) -> tuple[dict[str, np.ndarray], dict]:
    """Build sets that repeat one source image under nested fresh keys."""
    grouped: dict[str, list[int]] = {}
    for index, row in enumerate(metadata):
        if row["split"] == split:
            grouped.setdefault(str(row["identity_id"]), []).append(index)
    if not grouped:
        raise ValueError(f"No identities found for split {split!r}")

    flat_embeddings: list[np.ndarray] = []
    virtual_metadata: list[dict] = []
    targets, identity_ids, set_ids = [], [], []
    gallery, gallery_identity_ids = [], []
    for identity_id in sorted(grouped):
        indices = sorted(grouped[identity_id], key=lambda index: int(metadata[index]["sample_index"]))
        gallery_index, exposure_indices = indices[0], np.asarray(indices[1:])
        gallery.append(embeddings[gallery_index])
        gallery_identity_ids.append(identity_id)
        for repeat in range(set_config.repeats_per_identity):
            plan_seed = generate_key(set_config.seed, split, f"{identity_id}:{repeat}")
            source_index = int(np.random.default_rng(plan_seed).permutation(exposure_indices)[0])
            source = embeddings[source_index]
            targets.append(source)
            identity_ids.append(identity_id)
            set_ids.append(f"{split}:{identity_id}:{repeat}")
            for slot in range(set_config.exposures):
                flat_embeddings.append(source)
                virtual_metadata.append(
                    {"sample_id": f"same-image:{identity_id}:{repeat}:{slot}", "split": split}
                )

    protected, audit = protect_embeddings(
        np.asarray(flat_embeddings, dtype=np.float32),
        virtual_metadata,
        "independent_unseen_keys",
        key_seed,
        template_dim,
        protection,
    )
    set_count = len(targets)
    return {
        "templates": protected.reshape(set_count, set_config.exposures, -1),
        "targets": np.asarray(targets, dtype=np.float32),
        "identity_ids": np.asarray(identity_ids),
        "set_ids": np.asarray(set_ids),
        "gallery": np.asarray(gallery, dtype=np.float32),
        "gallery_identity_ids": np.asarray(gallery_identity_ids),
    }, audit


def make_model(model_name: str, input_dim: int, output_dim: int, hidden_dim: int):
    if model_name == "single_mlp":
        return SingleTemplateMLP(input_dim, output_dim, hidden_dim)
    if model_name == "mean_mlp":
        return PooledTemplateMLP(input_dim, output_dim, hidden_dim, "mean")
    if model_name == "max_mlp":
        return PooledTemplateMLP(input_dim, output_dim, hidden_dim, "max")
    if model_name == "deepsets":
        return DeepSetsExtractor(input_dim, output_dim, hidden_dim)
    raise ValueError(f"Unknown model: {model_name}")


def train_model(
    model_name: str,
    train_set: dict[str, np.ndarray],
    validation_set: dict[str, np.ndarray],
    test_set: dict[str, np.ndarray],
    training: dict,
    seed: int,
) -> dict:
    started = time.time()
    seed_record = seed_record_dict(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = make_model(
        model_name,
        train_set["templates"].shape[-1],
        train_set["targets"].shape[-1],
        int(training["hidden_dim"]),
    ).to(device)
    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=float(training["learning_rate"]),
        weight_decay=float(training["weight_decay"]),
    )
    train_inputs = torch.tensor(train_set["templates"], dtype=torch.float32, device=device)
    train_targets = torch.tensor(train_set["targets"], dtype=torch.float32, device=device)
    validation_inputs = torch.tensor(validation_set["templates"], dtype=torch.float32, device=device)
    validation_targets = torch.tensor(validation_set["targets"], dtype=torch.float32, device=device)
    best_state = copy.deepcopy(model.state_dict())
    best_validation_loss = float("inf")
    best_epoch = 0
    stale_epochs = 0
    for epoch in range(1, int(training["epochs"]) + 1):
        model.train()
        optimizer.zero_grad()
        predictions = model(train_inputs)
        loss = (1 - F.cosine_similarity(predictions, train_targets, dim=-1)).mean()
        loss = loss + float(training["mse_weight"]) * F.mse_loss(predictions, train_targets)
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            validation_predictions = model(validation_inputs)
            validation_loss = (1 - F.cosine_similarity(validation_predictions, validation_targets, dim=-1)).mean()
            validation_loss = validation_loss + float(training["mse_weight"]) * F.mse_loss(
                validation_predictions, validation_targets
            )
        if float(validation_loss) < best_validation_loss - 1e-6:
            best_validation_loss = float(validation_loss)
            best_epoch = epoch
            best_state = copy.deepcopy(model.state_dict())
            stale_epochs = 0
        else:
            stale_epochs += 1
            if stale_epochs >= int(training["patience"]):
                break

    model.load_state_dict(best_state)
    model.eval()
    with torch.no_grad():
        predictions = model(torch.tensor(test_set["templates"], dtype=torch.float32, device=device)).cpu().numpy()
    target_cosines = np.sum(predictions * test_set["targets"], axis=1)
    clustered_interval = identity_clustered_top1_interval(
        predictions,
        test_set["gallery"],
        test_set["identity_ids"],
        test_set["gallery_identity_ids"],
        seed=seed,
        n_resamples=int(training["bootstrap_resamples"]),
        confidence=float(training["bootstrap_confidence"]),
    )
    return {
        "seed": seed,
        "seed_record": seed_record,
        "device": str(device),
        "best_epoch": best_epoch,
        "best_validation_loss": best_validation_loss,
        "mean_target_cosine": float(target_cosines.mean()),
        "normalized_l2": float(np.linalg.norm(predictions - test_set["targets"], axis=1).mean()),
        "top1_identity_clustered_interval": clustered_interval,
        "elapsed_seconds": time.time() - started,
        **gallery_probe_metrics(
            predictions,
            test_set["gallery"],
            test_set["identity_ids"],
            test_set["gallery_identity_ids"],
        ),
    }


def aggregate_runs(runs: list[dict]) -> dict[str, dict[str, float]]:
    metrics = (
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
    return {
        metric: {
            "mean": float(np.mean([run[metric] for run in runs])),
            "std": float(np.std([run[metric] for run in runs], ddof=1)) if len(runs) > 1 else 0.0,
        }
        for metric in metrics
    }


def evaluate_primary_evidence(condition_results: dict, metadata: list[dict], config: dict) -> dict:
    chance = 1.0 / len({str(row["identity_id"]) for row in metadata if row["split"] == "test"})
    if config.get("primary_analysis") == "descriptive_control":
        control_model = str(config.get("control_model", "mean_mlp"))
        conditions = {}
        for condition, condition_result in condition_results.items():
            exposures = condition_result["exposures"]
            ten = exposures["10"]["models"][control_model]
            row = {"ten_record_top1_mean": ten["summary"]["top1_linkage"]["mean"]}
            if "1" in exposures:
                one = exposures["1"]["models"]["single_mlp"]
                row["one_record_top1_mean"] = one["summary"]["top1_linkage"]["mean"]
                row["multiplicity_amplification"] = row["ten_record_top1_mean"] - row["one_record_top1_mean"]
            conditions[condition] = row
        return {
            "analysis": "descriptive_control",
            "control": config.get("control_name", "unspecified"),
            "control_model": control_model,
            "chance_top1": chance,
            "conditions": conditions,
        }
    if config.get("primary_analysis") == "key_pool_boundary":
        fresh = condition_results["independent_unseen_keys"]["exposures"]["10"]["models"]["mean_mlp"]
        boundary = {}
        for condition in config["conditions"]:
            if not condition.startswith(("system_key_pool_", "random_key_pool_")):
                continue
            exposures = condition_results[condition]["exposures"]
            model = exposures["10"]["models"]["mean_mlp"]
            boundary[condition] = {
                "top1_mean": model["summary"]["top1_linkage"]["mean"],
                "all_clustered_intervals_exclude_chance": all(
                    run["top1_identity_clustered_interval"]["lower"] > chance for run in model["runs"]
                ),
            }
            if "1" in exposures:
                one_record = exposures["1"]["models"]["single_mlp"]["summary"]["top1_linkage"]["mean"]
                boundary[condition]["one_record_top1_mean"] = one_record
                boundary[condition]["multiplicity_amplification"] = boundary[condition]["top1_mean"] - one_record
        fresh_top1 = fresh["summary"]["top1_linkage"]["mean"]
        minimum_effect = float(config["amplification_threshold"])
        return {
            "analysis": "key_pool_boundary",
            "chance_top1": chance,
            "fresh_key_top1_mean": fresh_top1,
            "ten_exposure_mean_pool_boundary": boundary,
            "all_recurring_pools_exclude_chance": all(
                row["all_clustered_intervals_exclude_chance"] for row in boundary.values()
            ),
            "all_recurring_pools_meet_minimum_effect": all(
                row["top1_mean"] - fresh_top1 >= minimum_effect for row in boundary.values()
            ),
        }

    primary = condition_results["independent_unseen_keys"]["exposures"]
    level_one = primary["1"]["models"]["single_mlp"]
    level_ten = primary["10"]["models"]["deepsets"]
    increase = level_ten["summary"]["top1_linkage"]["mean"] - level_one["summary"]["top1_linkage"]["mean"]
    all_intervals_exclude_chance = all(run["top1_identity_clustered_interval"]["lower"] > chance for run in level_ten["runs"])
    return {
        "analysis": "exposure_amplification",
        "chance_top1": chance,
        "level_1_top1_mean": level_one["summary"]["top1_linkage"]["mean"],
        "level_10_deepsets_top1_mean": level_ten["summary"]["top1_linkage"]["mean"],
        "absolute_increase": increase,
        "all_level_10_clustered_intervals_exclude_chance": all_intervals_exclude_chance,
        "minimum_effect_met": increase >= float(config["amplification_threshold"]),
        "exposure_amplification_detected": all_intervals_exclude_chance and increase >= float(config["amplification_threshold"]),
    }


def run(config: dict) -> dict:
    if config.get("classification") != "exploratory independent study, not benchmark_cb reproduction":
        raise ValueError("The real multi-exposure classification must remain explicit")
    started = time.time()
    embeddings, metadata, embedding_manifest = load_embeddings(Path(config["embedding_dir"]))
    if config.get("split_reassignment_seed") is not None:
        metadata = reassign_identity_splits(metadata, int(config["split_reassignment_seed"]))
    condition_results = {}
    for condition in config["conditions"]:
        same_image_mode = config.get("exposure_mode") == "same_image_different_keys"
        if same_image_mode and condition != "independent_unseen_keys":
            raise ValueError("same_image_different_keys supports only independent_unseen_keys")
        if not same_image_mode:
            protected, key_audit = protect_embeddings(
                embeddings,
                metadata,
                condition,
                int(config["key_seed"]),
                int(config["template_dim"]),
                config.get("protection"),
            )
        exposure_results = {}
        for exposures in config["exposures"]:
            set_config = ExposureSetConfig(int(exposures), int(config["repeats_per_identity"]), int(config["set_seed"]))
            if same_image_mode:
                train_set, train_audit = build_same_image_different_key_sets(
                    embeddings, metadata, "train", set_config, int(config["key_seed"]),
                    int(config["template_dim"]), config.get("protection")
                )
                validation_set, validation_audit = build_same_image_different_key_sets(
                    embeddings, metadata, "val", set_config, int(config["key_seed"]),
                    int(config["template_dim"]), config.get("protection")
                )
                test_set, test_audit = build_same_image_different_key_sets(
                    embeddings, metadata, "test", set_config, int(config["key_seed"]),
                    int(config["template_dim"]), config.get("protection")
                )
                key_audit = {
                    "scheme": train_audit["scheme"],
                    "unique_keys_at_level": (
                        train_audit["unique_keys"] + validation_audit["unique_keys"] + test_audit["unique_keys"]
                    ),
                    "split_key_disjoint": True,
                    "exposure_mode": "same image with different fresh keys",
                }
            else:
                train_set = build_real_exposure_sets(embeddings, protected, metadata, "train", set_config)
                validation_set = build_real_exposure_sets(embeddings, protected, metadata, "val", set_config)
                test_set = build_real_exposure_sets(embeddings, protected, metadata, "test", set_config)
            if config.get("record_control") == "shuffle_non_anchor":
                train_set = shuffle_non_anchor_records(
                    train_set, generate_key(int(config["set_seed"]), "shuffle", f"{condition}:train:{exposures}")
                )
                validation_set = shuffle_non_anchor_records(
                    validation_set, generate_key(int(config["set_seed"]), "shuffle", f"{condition}:val:{exposures}")
                )
                test_set = shuffle_non_anchor_records(
                    test_set, generate_key(int(config["set_seed"]), "shuffle", f"{condition}:test:{exposures}")
                )
            elif config.get("record_control") not in (None, "none"):
                raise ValueError(f"Unknown record_control: {config['record_control']}")
            model_names = ["single_mlp"] if int(exposures) == 1 else list(config["models"])
            models = {}
            for model_name in model_names:
                runs = [
                    train_model(model_name, train_set, validation_set, test_set, config["training"], int(seed))
                    for seed in config["training"]["seeds"]
                ]
                models[model_name] = {"runs": runs, "summary": aggregate_runs(runs)}
            exposure_results[str(exposures)] = {
                "set_counts": {
                    "train": len(train_set["templates"]),
                    "val": len(validation_set["templates"]),
                    "test": len(test_set["templates"]),
                },
                "unprotected_oracle": gallery_probe_metrics(
                    test_set["targets"],
                    test_set["gallery"],
                    test_set["identity_ids"],
                    test_set["gallery_identity_ids"],
                ),
                "models": models,
            }
        condition_results[condition] = {"key_audit": key_audit, "exposures": exposure_results}

    evidence = evaluate_primary_evidence(condition_results, metadata, config)
    return {
        "classification": config["classification"],
        "dataset": config["dataset"],
        "protection": config.get("protection", {"scheme": "biohash"}),
        "record_control": config.get("record_control", "none"),
        "exposure_mode": config.get("exposure_mode", "different_images"),
        "split_reassignment_seed": config.get("split_reassignment_seed"),
        "split_identity_counts": {
            split: len({str(row["identity_id"]) for row in metadata if row["split"] == split})
            for split in ("train", "val", "test")
        },
        "embedding_manifest": embedding_manifest,
        "conditions": condition_results,
        "primary_evidence": evidence,
        "software": {"numpy": version("numpy"), "torch": version("torch"), "scikit-learn": version("scikit-learn")},
        "git_commit": subprocess.run(["git", "rev-parse", "HEAD"], text=True, capture_output=True).stdout.strip(),
        "elapsed_seconds": time.time() - started,
    }


def write_results(config: dict, result: dict) -> None:
    output = Path(config["results_dir"])
    output.mkdir(parents=True, exist_ok=True)
    (output / "run_config.yaml").write_text(yaml.safe_dump(config, sort_keys=True), encoding="utf-8")
    (output / "metrics.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    with (output / "summary.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["condition", "exposures", "model", "metric", "mean", "std"])
        for condition, condition_result in result["conditions"].items():
            for exposures, exposure_result in condition_result["exposures"].items():
                for model_name, model_result in exposure_result["models"].items():
                    for metric, statistics in model_result["summary"].items():
                        writer.writerow([condition, exposures, model_name, metric, statistics["mean"], statistics["std"]])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    result = run(config)
    write_results(config, result)
    print(json.dumps({"results_dir": config["results_dir"], "primary_evidence": result["primary_evidence"]}, indent=2))


if __name__ == "__main__":
    main()
