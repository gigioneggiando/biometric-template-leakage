"""Replicate recurring pools with a matched prediction-averaging baseline."""
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
import zipfile

import numpy as np
import torch
from torch.nn import functional as functional
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from scripts.train import run_real_multiexposure as runner
from scripts.train.run_scheme_extension_pilot import write_table


def pool_interval(scores: np.ndarray, seed: int, resamples: int) -> tuple[float, float]:
    scores = np.asarray(scores, dtype=float)
    if scores.ndim != 3 or min(scores.shape) < 2 or not np.isfinite(scores).all() or resamples < 1:
        raise ValueError("Expected finite pool by model-seed by identity scores")
    rng = np.random.default_rng(seed)
    pools = rng.integers(scores.shape[0], size=(resamples, scores.shape[0]))
    seeds = rng.integers(scores.shape[1], size=(resamples, scores.shape[1]))
    identities = rng.integers(scores.shape[2], size=(resamples, scores.shape[2]))
    estimates = scores[pools[:, :, None, None], seeds[:, None, :, None], identities[:, None, None, :]].mean(axis=(1, 2, 3))
    return tuple(float(value) for value in np.quantile(estimates, [0.025, 0.975]))


def predict(model: torch.nn.Module, templates: np.ndarray, *, average_records: bool = False) -> np.ndarray:
    device = next(model.parameters()).device
    values = torch.as_tensor(templates, dtype=torch.float32, device=device)
    if values.ndim != 3 or values.shape[1] < 1:
        raise ValueError("Expected nonempty batch by records by features")
    model.eval()
    with torch.no_grad():
        if average_records:
            predictions = model(values.reshape(-1, 1, values.shape[-1]))
            predictions = predictions.reshape(values.shape[0], values.shape[1], -1).mean(dim=1)
            predictions = functional.normalize(predictions, dim=-1)
        else:
            predictions = model(values)
    return predictions.cpu().numpy()


def fit_model(model_name: str, train_set: dict, validation_set: dict, training: dict, seed: int):
    runner.seed_record_dict(seed)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = runner.make_model(model_name, train_set["templates"].shape[-1], train_set["targets"].shape[-1],
                              int(training["hidden_dim"])).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=float(training["learning_rate"]),
                                 weight_decay=float(training["weight_decay"]))
    train_inputs = torch.tensor(train_set["templates"], dtype=torch.float32, device=device)
    train_targets = torch.tensor(train_set["targets"], dtype=torch.float32, device=device)
    validation_inputs = torch.tensor(validation_set["templates"], dtype=torch.float32, device=device)
    validation_targets = torch.tensor(validation_set["targets"], dtype=torch.float32, device=device)
    best_state = copy.deepcopy(model.state_dict())
    best_loss, best_epoch, stale_epochs = float("inf"), 0, 0
    for epoch in range(1, int(training["epochs"]) + 1):
        if time.monotonic() >= training.get("deadline_monotonic", float("inf")):
            raise TimeoutError("Independent-pool budget exhausted")
        model.train()
        optimizer.zero_grad()
        predictions = model(train_inputs)
        loss = (1 - functional.cosine_similarity(predictions, train_targets, dim=-1)).mean()
        loss = loss + float(training["mse_weight"]) * functional.mse_loss(predictions, train_targets)
        loss.backward()
        optimizer.step()
        model.eval()
        with torch.no_grad():
            predictions = model(validation_inputs)
            loss = (1 - functional.cosine_similarity(predictions, validation_targets, dim=-1)).mean()
            loss = loss + float(training["mse_weight"]) * functional.mse_loss(predictions, validation_targets)
        if float(loss) < best_loss - 1e-6:
            best_loss, best_epoch, stale_epochs = float(loss), epoch, 0
            best_state = copy.deepcopy(model.state_dict())
        else:
            stale_epochs += 1
            if stale_epochs >= int(training["patience"]):
                break
    model.load_state_dict(best_state)
    model.eval()
    return model, {"best_epoch": best_epoch, "best_validation_loss": best_loss}


def analyse(records: list[dict], config: dict) -> None:
    public, contrasts, per_pool = [], [], []
    for record in records:
        public.append({key: value for key, value in record.items() if key != "identity_scores"})
    groups = sorted({(row["dataset"], row["scheme"], row["split_seed"]) for row in records})
    for dataset, scheme, split in groups:
        selected = [row for row in records if (row["dataset"], row["scheme"], row["split_seed"]) == (dataset, scheme, split)]
        lookup = {(row["key_seed"], row["model_seed"], row["model"]): row for row in selected}
        pools = sorted({row["key_seed"] for row in selected})
        seeds = sorted({row["model_seed"] for row in selected})
        identities = sorted(selected[0]["identity_scores"])
        if any(sorted(row["identity_scores"]) != identities for row in selected):
            raise ValueError("Identity clusters differ within a partition")
        if len(lookup) != len(selected) or len(selected) != len(pools) * len(seeds) * 3:
            raise ValueError("Incomplete or duplicate model/pool matrix")
        if len(pools) != 3 or len(seeds) != 3:
            continue
        matrices = {model: np.asarray([[[lookup[(pool, seed, model)]["identity_scores"][identity]
                                       for identity in identities] for seed in seeds] for pool in pools])
                    for model in ("single_mlp", "mean_mlp", "prediction_mean")}
        common = {"dataset": dataset, "scheme": scheme, "split_seed": split, "pools": len(pools),
                  "model_seeds": len(seeds), "identities": len(identities), "chance": 1 / len(identities)}
        for contrast, reference in (("mean10_minus_single1", "single_mlp"), ("mean10_minus_prediction10", "prediction_mean")):
            difference = matrices["mean_mlp"] - matrices[reference]
            lower, upper = pool_interval(difference, config["analysis_seed"], config["bootstrap_resamples"])
            pool_gains = difference.mean(axis=(1, 2))
            contrasts.append({**common, "contrast": contrast, "gain": float(difference.mean()),
                              "lower95": lower, "upper95": upper, "min_pool_gain": float(pool_gains.min()),
                              "max_pool_gain": float(pool_gains.max()), "positive_pools": int((pool_gains > 0).sum()),
                              "mean10_top1": float(matrices["mean_mlp"].mean()),
                              "reference_top1": float(matrices[reference].mean()),
                              "inference": "pointwise pool/seed/identity bootstrap; no corrected significance claim"})
            for pool_index, pool in enumerate(pools):
                per_pool.append({**common, "key_seed": pool, "contrast": contrast,
                                 "gain": float(pool_gains[pool_index]),
                                 "mean10_top1": float(matrices["mean_mlp"][pool_index].mean()),
                                 "reference_top1": float(matrices[reference][pool_index].mean())})
    destination = Path(config["summary_dir"])
    write_table(destination / "results_summary.csv", public)
    write_table(destination / "pool_contrasts.csv", per_pool)
    write_table(destination / "crossed_contrasts.csv", contrasts)


def execute(config_path: Path) -> None:
    config = yaml.safe_load(config_path.read_text())
    base = yaml.safe_load(Path(config["base_config"]).read_text())
    if not 0 < config["max_wall_seconds"] <= 3600 or len(set(config["key_seeds"])) != 3:
        raise ValueError("Expected three independent pool seeds and at most one hour")
    destination, private = Path(config["summary_dir"]), Path(config["output_root"])
    destination.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)
    manifest_path = destination / "execution_manifest.json"
    if manifest_path.exists() or any(private.iterdir()):
        raise FileExistsError("Execution already exists; use a new study path")
    sources = sorted(set([config_path.resolve(), Path(config["base_config"]).resolve(), Path(config["protocol"]).resolve()]
                         + list((ROOT / "src/biometrics_ai").rglob("*.py"))
                         + list((ROOT / "scripts/train").glob("*.py"))))
    hashes = {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    inputs = {str(Path(dataset["embedding_dir"]) / filename).replace("\\", "/"):
              hashlib.sha256((Path(dataset["embedding_dir"]) / filename).read_bytes()).hexdigest()
              for dataset in base["datasets"] for filename in ("embeddings.npy", "metadata.json", "embedding_manifest.json")}
    with zipfile.ZipFile(destination / "executed_sources.zip", "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sources:
            archive.write(path, path.relative_to(ROOT).as_posix())
    manifest = {"started_utc": datetime.now(timezone.utc).isoformat(), "status": "running", "config": config,
                "base_commit": subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip(),
                "source_sha256": hashes, "input_sha256": inputs, "torch_threads": 8,
                "software": {name: version(name) for name in ("numpy", "torch", "scipy", "scikit-learn", "PyYAML")},
                "planned_cells": 24, "planned_trained_endpoints": 144, "planned_evaluated_endpoints": 216}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    torch.set_num_threads(8)
    started = time.monotonic()
    deadline = started + config["max_wall_seconds"]
    records, completed = [], 0
    try:
        for dataset in base["datasets"]:
            embeddings, metadata, _ = runner.load_embeddings(Path(dataset["embedding_dir"]))
            if not np.isfinite(embeddings).all() or not np.allclose(np.linalg.norm(embeddings, axis=1), 1, atol=1e-4):
                raise ValueError("Expected finite unit embeddings")
            metadata = runner.reassign_identity_splits(metadata, dataset["split_reassignment_seed"])
            for scheme in base["schemes"]:
                for key_seed in config["key_seeds"]:
                    if time.monotonic() >= deadline:
                        raise TimeoutError("Study budget exhausted")
                    cell_started = time.monotonic()
                    protected, _ = runner.protect_embeddings(embeddings, metadata, config["condition"], key_seed,
                                                             scheme["template_dim"], scheme["protection"])
                    sets = {exposure: {split: runner.build_real_exposure_sets(embeddings, protected, metadata, split,
                                      runner.ExposureSetConfig(exposure, base["repeats_per_identity"], base["set_seed"]))
                                      for split in ("train", "val", "test")} for exposure in (1, 10)}
                    if not np.array_equal(sets[1]["test"]["set_ids"], sets[10]["test"]["set_ids"]):
                        raise ValueError("Nested exposure sets do not align")
                    training = {**base["training"], "deadline_monotonic": deadline}
                    cell_records = []
                    for seed in training["seeds"]:
                        for model_name, exposure in (("single_mlp", 1), ("mean_mlp", 10)):
                            fit_started = time.monotonic()
                            model, training_info = fit_model(model_name, sets[exposure]["train"], sets[exposure]["val"], training, seed)
                            fit_seconds = time.monotonic() - fit_started
                            endpoints = [(model_name, exposure, False)]
                            if model_name == "single_mlp":
                                endpoints.append(("prediction_mean", 10, True))
                            for label, test_exposure, average in endpoints:
                                test_set = sets[test_exposure]["test"]
                                predictions = predict(model, test_set["templates"], average_records=average)
                                scores = runner.identity_top1_scores(predictions, test_set)
                                cell_records.append({"dataset": dataset["name"], "scheme": scheme["name"],
                                                     "split_seed": dataset["split_reassignment_seed"], "key_seed": key_seed,
                                                     "model_seed": seed, "model": label, "exposures": test_exposure,
                                                     "top1": float(np.mean(list(scores.values()))),
                                                     "chance": 1 / len(scores), **training_info,
                                                     "training_seconds": fit_seconds if label != "prediction_mean" else 0,
                                                     "identity_scores": scores})
                    records.extend(cell_records)
                    completed += 1
                    cell_name = f"{dataset['name']}_{scheme['name']}_{dataset['split_reassignment_seed']}_{key_seed}.json"
                    (private / cell_name).write_text(json.dumps(cell_records, indent=2) + "\n")
                    analyse(records, config)
                    print(f"Completed {completed}/24: {cell_name} ({time.monotonic() - cell_started:.1f}s)", flush=True)
        manifest["status"] = "completed"
    except Exception:
        manifest["status"] = "failed_or_partial"
        raise
    finally:
        manifest.update(completed_cells=completed, evaluated_endpoints=len(records),
                        wall_seconds=time.monotonic() - started, finished_utc=datetime.now(timezone.utc).isoformat())
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=ROOT / "configs/attacks/pool_replication_2026-09-19.yaml")
    execute(parser.parse_args().config)