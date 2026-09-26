"""Post-hoc descriptive diagnostics for the frozen MOBIO/SCface utility study."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import sys

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from scripts.train import run_scface_utility_confirmation as study
from scripts.train import run_source_security_utility as pilot
from scripts.train.run_scheme_extension_pilot import write_table


DESTINATION = ROOT / "experiments/utility_failure_diagnostics_2026-09-26"


def tree_digest(paths: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(paths):
        digest.update(path.name.encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def read_record(private_root: Path, dataset: str, split: int, seed: int, policy: str) -> dict:
    return json.loads((private_root / f"{dataset}_{split}_{seed}_{policy}.json").read_text())


def paired_arrays(private_root: Path, dataset: str, split: int):
    before = [read_record(private_root, dataset, split, seed, "recurring") for seed in study.SEEDS]
    after = [read_record(private_root, dataset, split, seed, "separated") for seed in study.SEEDS]
    identities = before[0]["utility"]["identities"]
    if any(record["utility"]["identities"] != identities for record in before + after):
        raise ValueError("Identity order differs across paired records")
    baseline = np.asarray([record["utility"]["identity_tar"] for record in before])
    candidate = np.asarray([record["utility"]["identity_tar"] for record in after])
    return before, after, identities, baseline, candidate


def variability_rows(private_root: Path) -> tuple[list[dict], dict]:
    rows = []
    identity_sets = {}
    for dataset in study.DATASETS:
        for split in study.SPLITS:
            before, after, identities, baseline, candidate = paired_arrays(private_root, dataset, split)
            differences = candidate - baseline
            identity_means = differences.mean(axis=0)
            seed_means = differences.mean(axis=1)
            identity_sets[(dataset, split)] = set(identities)
            rows.append({
                "dataset": dataset,
                "split_seed": split,
                "identities": len(identities),
                "key_seeds": len(study.SEEDS),
                "mean_difference": float(differences.mean()),
                "identity_axis_sd": float(identity_means.std(ddof=1)),
                "seed_axis_sd": float(seed_means.std(ddof=1)),
                "identity_mean_min": float(identity_means.min()),
                "identity_mean_max": float(identity_means.max()),
                "negative_identity_fraction": float(np.mean(identity_means < 0)),
                "seed_mean_min": float(seed_means.min()),
                "seed_mean_max": float(seed_means.max()),
                "negative_seed_fraction": float(np.mean(seed_means < 0)),
                "baseline_candidate_correlation": float(np.corrcoef(baseline.ravel(), candidate.ravel())[0, 1]),
                "mean_threshold_difference": float(np.mean([
                    candidate_record["utility"]["threshold"] - baseline_record["utility"]["threshold"]
                    for baseline_record, candidate_record in zip(before, after)
                ])),
            })
    overlaps = {
        dataset: {
            "test_identities_per_split": len(identity_sets[(dataset, study.SPLITS[0])]),
            "overlap": len(identity_sets[(dataset, study.SPLITS[0])] & identity_sets[(dataset, study.SPLITS[1])]),
        }
        for dataset in study.DATASETS
    }
    return rows, overlaps


def scface_capture_rows(data_root: Path, private_root: Path) -> list[dict]:
    embeddings, original, _ = pilot.runner.load_embeddings(data_root / study.DATASETS["SCface"])
    output = []
    for split in study.SPLITS:
        metadata = pilot.runner.reassign_identity_splits(original, split)
        identity_ids = sorted({str(row["identity_id"]) for row in metadata if row["split"] == "test"})
        groups = {
            identity: sorted(
                [index for index, row in enumerate(metadata)
                 if row["split"] == "test" and str(row["identity_id"]) == identity],
                key=lambda index: int(metadata[index]["sample_index"]),
            )
            for identity in identity_ids
        }
        seed_rates: dict[tuple[str, str, str], list[float]] = {}
        for seed in study.SEEDS:
            for policy in ("recurring", "separated"):
                record = read_record(private_root, "SCface", split, seed, policy)
                threshold = float(record["utility"]["threshold"])
                accepted_by_identity = []
                grouped_acceptance: dict[tuple[str, str], list[bool]] = {}
                distance_acceptance: dict[str, list[bool]] = {}
                for identity in identity_ids:
                    indices = groups[identity]
                    enrollment, probes = indices[0], indices[1:]
                    transform = pilot.projection(policy, seed, enrollment)
                    gallery = embeddings[enrollment] @ transform >= 0
                    scores = np.mean((embeddings[probes] @ transform >= 0) == gallery, axis=1)
                    accepted = scores >= threshold
                    accepted_by_identity.append(float(accepted.mean()))
                    for index, decision in zip(probes, accepted):
                        camera = str(metadata[index].get("camera_id", "unknown"))
                        distance = str(metadata[index].get("distance_id", "unknown"))
                        grouped_acceptance.setdefault((camera, distance), []).append(bool(decision))
                        distance_acceptance.setdefault(distance, []).append(bool(decision))
                if not np.isclose(np.mean(accepted_by_identity), record["utility"]["tar"]):
                    raise ValueError("Capture diagnostic does not reproduce frozen SCface TAR")
                for (camera, distance), decisions in grouped_acceptance.items():
                    seed_rates.setdefault((policy, camera, distance), []).append(float(np.mean(decisions)))
                for distance, decisions in distance_acceptance.items():
                    seed_rates.setdefault((policy, "all", distance), []).append(float(np.mean(decisions)))
        groups = sorted({(camera, distance) for _, camera, distance in seed_rates})
        for camera, distance in groups:
            baseline = np.asarray(seed_rates[("recurring", camera, distance)])
            candidate = np.asarray(seed_rates[("separated", camera, distance)])
            output.append({
                "split_seed": split,
                "camera": camera,
                "distance": distance,
                "aggregation": "distance" if camera == "all" else "camera_distance",
                "key_seeds": len(study.SEEDS),
                "baseline_tar": float(baseline.mean()),
                "candidate_tar": float(candidate.mean()),
                "mean_difference": float((candidate - baseline).mean()),
                "seed_difference_sd": float((candidate - baseline).std(ddof=1)),
                "seed_difference_min": float((candidate - baseline).min()),
                "seed_difference_max": float((candidate - baseline).max()),
            })
    return output


def execute(data_root: Path, private_root: Path, destination: Path = DESTINATION) -> dict:
    outputs = ["variability.csv", "scface_capture.csv", "summary.json", "execution_manifest.json"]
    if any((destination / name).exists() for name in outputs):
        raise FileExistsError("Refusing to overwrite utility diagnostics")
    private_files = sorted(private_root.glob("*.json"))
    if len(private_files) != 96:
        raise ValueError("Expected 96 frozen private endpoint files")
    variability, overlaps = variability_rows(private_root)
    captures = scface_capture_rows(data_root, private_root)
    distance_rows = [row for row in captures if row["aggregation"] == "distance"]
    summary = {
        "status": "completed",
        "scope": "post-hoc descriptive diagnosis; frozen utility decisions unchanged",
        "variability_cells": len(variability),
        "scface_capture_cells": len(captures),
        "split_overlap": overlaps,
        "scface_distance_extremes": {
            str(split): {
                "lowest_candidate_tar_distance": min(
                    (row for row in distance_rows if row["split_seed"] == split),
                    key=lambda row: row["candidate_tar"],
                )["distance"],
                "highest_candidate_tar_distance": max(
                    (row for row in distance_rows if row["split_seed"] == split),
                    key=lambda row: row["candidate_tar"],
                )["distance"],
            }
            for split in study.SPLITS
        },
    }
    destination.mkdir(parents=True)
    write_table(destination / "variability.csv", variability)
    write_table(destination / "scface_capture.csv", captures)
    (destination / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    metadata_path = data_root / study.DATASETS["SCface"] / "metadata.json"
    embeddings_path = data_root / study.DATASETS["SCface"] / "embeddings.npy"
    manifest = {
        "status": "completed",
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "private_endpoint_bundle_sha256": tree_digest(private_files),
        "scface_metadata_sha256": hashlib.sha256(metadata_path.read_bytes()).hexdigest(),
        "scface_embeddings_sha256": hashlib.sha256(embeddings_path.read_bytes()).hexdigest(),
        "private_files_read": len(private_files),
        "private_identity_rows_exported": 0,
    }
    (destination / "execution_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--private-root", type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(execute(args.data_root.resolve(), args.private_root.resolve()), indent=2))


if __name__ == "__main__":
    main()
