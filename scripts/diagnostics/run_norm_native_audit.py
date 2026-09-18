"""Hash-frozen natural-norm, independent matching and failure-analysis revision."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np
from scipy.spatial.distance import cdist
from scipy.stats import permutation_test
import yaml

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from biometrics_ai.face.arcface import OpenCvYuNetArcFaceExtractor, _ARCFACE_DESTINATION, _similarity_transform
from biometrics_ai.protection import generate_key
from biometrics_ai.protection.iomgrp import IoMGRPConfig, iomgrp_batch
from biometrics_ai.protection.polyprotect import PolyProtectConfig, polyprotect_parameters
from scripts.train import run_real_multiexposure as runner
from scripts.train.run_scheme_extension_pilot import write_table
from scripts.train.run_scheme_followup import crossed_interval, holm_adjust, native_null_test

DESTINATION = ROOT / "experiments/norm_native_audit_2026-09-18"
PRIVATE = ROOT / "results/norm_native_audit_2026-09-18"
SEED = 91903
PERMUTATIONS = 4999
RESAMPLES = 4000


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_deadline(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise TimeoutError("Frozen revision budget exhausted")


def scalar_polyprotect(vector: np.ndarray, coefficients: np.ndarray, exponents: np.ndarray,
                       overlap: int = 2) -> tuple[np.ndarray, np.ndarray]:
    full, linear, offset = [], [], 0
    width = len(coefficients)
    while True:
        terms = [float(coefficients[position]) *
                 (float(vector[offset + position]) if offset + position < len(vector) else 0.0)
                 ** int(exponents[position]) for position in range(width)]
        full.append(sum(terms))
        linear.append(sum(term for term, exponent in zip(terms, exponents) if exponent == 1))
        if offset + width >= len(vector):
            break
        offset += width - overlap
    return np.asarray(full, dtype=np.float32), np.asarray(linear, dtype=np.float32)


def gallery_protocol(metadata: list[dict]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    identities = sorted({str(row["identity_id"]) for row in metadata})
    if len({row["sample_id"] for row in metadata}) != len(metadata):
        raise ValueError("Duplicate source records")
    gallery, probes, labels = [], [], []
    for label, identity in enumerate(identities):
        members = sorted([index for index, row in enumerate(metadata) if str(row["identity_id"]) == identity],
                         key=lambda index: int(metadata[index]["sample_index"]))
        if len(members) < 2:
            raise ValueError("Each identity needs gallery and probe records")
        gallery.append(members[0])
        probes.extend(members[1:])
        labels.extend([label] * (len(members) - 1))
    assert not set(gallery) & set(probes)
    return np.asarray(gallery), np.asarray(probes), np.asarray(labels)


def confusion_from_scores(scores: np.ndarray, labels: np.ndarray) -> np.ndarray:
    if not np.isfinite(scores).all() or scores.ndim != 2 or len(scores) != len(labels):
        raise ValueError("Invalid finite score matrix")
    predicted = scores.argmax(axis=1)
    return np.stack([np.bincount(predicted[labels == label], minlength=scores.shape[1]) /
                     (labels == label).sum() for label in range(scores.shape[1])])


def native_confusion(templates: np.ndarray, metadata: list[dict]) -> tuple[np.ndarray, dict]:
    gallery, probes, labels = gallery_protocol(metadata)
    values = templates.astype(np.float64)
    norms = np.linalg.norm(values, axis=1)
    if not np.isfinite(values).all() or np.any(norms == 0):
        raise ValueError("Nonfinite or zero protected template")
    values /= norms[:, None]
    scores = values[probes] @ values[gallery].T
    alternate = 1 - cdist(templates[probes].astype(float), templates[gallery].astype(float), metric="cosine")
    np.testing.assert_allclose(scores, alternate, rtol=1e-10, atol=1e-12)
    predictions = scores.argmax(axis=1)
    reverse = np.arange(len(gallery))[::-1]
    reordered = reverse[scores[:, reverse].argmax(axis=1)]
    ties = (np.isclose(scores, scores.max(axis=1, keepdims=True), rtol=0, atol=1e-12).sum(axis=1) > 1)
    audit = {"matcher_max_abs_error": float(np.max(np.abs(scores - alternate))),
             "matcher_prediction_disagreements": int(np.sum(predictions != alternate.argmax(axis=1))),
             "gallery_order_disagreements": int(np.sum(predictions != reordered)),
             "top_score_ties": int(ties.sum()), "probe_count": len(probes),
             "gallery_count": len(gallery), "gallery_probe_overlap": 0}
    return confusion_from_scores(scores, labels), audit


def identity_interval(scores: np.ndarray) -> tuple[float, float]:
    rng = np.random.default_rng(SEED)
    estimates = scores[rng.integers(len(scores), size=(RESAMPLES, len(scores)))].mean(axis=1)
    return tuple(float(value) for value in np.quantile(estimates, [0.025, 0.975]))


def signflip(scores: np.ndarray) -> float:
    if np.allclose(scores, 0):
        return 1.0
    return float(permutation_test((scores,), np.mean, permutation_type="samples", vectorized=True,
                                 alternative="two-sided", n_resamples=PERMUTATIONS,
                                 rng=np.random.default_rng(SEED)).pvalue)


def extract_raw(dataset: dict, deadline: float) -> tuple[np.ndarray, np.ndarray, list[dict], dict]:
    directory = ROOT / dataset["embedding_dir"]
    unit, metadata, manifest = runner.load_embeddings(directory)
    models = manifest["model_files"]
    for model in models.values():
        if digest(Path(model["path"])) != model["sha256"]:
            raise ValueError("Extraction model hash mismatch")
    extractor = OpenCvYuNetArcFaceExtractor(models["recognition"]["path"], models["detection"]["path"])
    import cv2
    cv2.setNumThreads(4)
    cache = PRIVATE / dataset["name"]
    cache.mkdir(parents=True, exist_ok=True)
    vectors = []
    for index, record in enumerate(metadata):
        check_deadline(deadline)
        image = cv2.imread(record["source_image"])
        if image is None:
            raise ValueError(f"Authorized image unavailable at record index {index}")
        landmarks = extractor._detect_largest(image)
        aligned = cv2.warpAffine(image, _similarity_transform(landmarks, _ARCFACE_DESTINATION), (112, 112), borderValue=0.0)
        extractor._recognizer.setInput(cv2.dnn.blobFromImage(aligned, 1 / 127.5, (112, 112), (127.5, 127.5, 127.5), swapRB=True))
        vector = np.asarray(extractor._recognizer.forward(), dtype=np.float32).reshape(-1)
        if vector.shape != (512,) or not np.isfinite(vector).all() or np.linalg.norm(vector) == 0:
            raise ValueError("Invalid raw ArcFace output")
        vectors.append(vector)
        if (index + 1) % 300 == 0:
            print(f"Raw extraction {dataset['name']}: {index + 1}/{len(metadata)}", flush=True)
    raw = np.stack(vectors)
    norms = np.linalg.norm(raw, axis=1)
    discrepancy = float(np.max(np.abs(raw / norms[:, None] - unit)))
    if discrepancy > 1e-4:
        raise ValueError(f"Re-extraction disagrees with frozen embeddings: {discrepancy}")
    np.save(cache / "raw_embeddings.npy", raw)
    audit = {"dataset": dataset["name"], "records": len(raw), "normalization_max_abs_error": discrepancy,
             "raw_norm_min": float(norms.min()), "raw_norm_median": float(np.median(norms)),
             "raw_norm_max": float(norms.max()), "raw_embeddings_sha256": digest(cache / "raw_embeddings.npy"),
             "saved_unit_sha256": digest(directory / "embeddings.npy"),
             "metadata_sha256": digest(directory / "metadata.json"),
             "recognition_sha256": models["recognition"]["sha256"], "detection_sha256": models["detection"]["sha256"]}
    return raw, unit, metadata, audit


def evaluate_dataset(dataset: str, raw: np.ndarray, unit: np.ndarray, metadata: list[dict],
                     deadline: float, tables: dict[str, list[dict]]) -> None:
    config = PolyProtectConfig()
    norms = np.linalg.norm(raw, axis=1)
    for split_seed in (91831, 91843):
        records = runner.reassign_identity_splits(metadata, split_seed)
        test_indices = np.asarray([index for index, row in enumerate(records) if row["split"] == "test"])
        test_records = [records[index] for index in test_indices]
        train_indices = [index for index, row in enumerate(records) if row["split"] == "train"]
        shuffled_norms = norms.copy()
        rng = np.random.default_rng(91901)
        for split in ("train", "val", "test"):
            indices = np.asarray([index for index, row in enumerate(records) if row["split"] == split])
            shuffled_norms[indices] = rng.permutation(norms[indices])
        arms = {"unit": unit[test_indices], "raw": raw[test_indices],
                "norm_shuffled": unit[test_indices] * shuffled_norms[test_indices, None],
                "fixed_radius": unit[test_indices] * np.median(norms[train_indices])}
        common = {"dataset": dataset, "split_seed": split_seed}
        means = {}
        for arm, values in arms.items():
            matrices, linear_matrices = [], []
            for key_seed in (91873, 91879, 91883):
                check_deadline(deadline)
                templates, key_audit = runner.protect_embeddings(values, test_records, "independent_unseen_keys", key_seed,
                    170, {"scheme": "polyprotect_paper_specified", "window_size": 5, "overlap": 2, "coefficient_bound": 50})
                reference, linear = [], []
                for vector, record in zip(values, test_records):
                    key = generate_key(key_seed, str(record["split"]), str(record["sample_id"]))
                    full, first = scalar_polyprotect(vector, *polyprotect_parameters(key, config))
                    reference.append(full)
                    linear.append(first)
                reference, linear = np.stack(reference), np.stack(linear)
                np.testing.assert_allclose(templates, reference, rtol=3e-6, atol=2e-5)
                confusion, matching_audit = native_confusion(reference, test_records)
                production_confusion, _ = native_confusion(templates, test_records)
                np.testing.assert_array_equal(confusion, production_confusion)
                linear_confusion, _ = native_confusion(linear, test_records)
                matrices.append(confusion)
                linear_matrices.append(linear_confusion)
                relative = np.linalg.norm(reference - linear, axis=1) / np.linalg.norm(reference, axis=1)
                tables["implementation_audit"].append({**common, "arm": arm, "key_seed": key_seed,
                    "records": len(values), "unique_keys": key_audit["unique_keys"],
                    "reference_max_abs_error": float(np.max(np.abs(templates - reference))),
                    "nonlinear_residual_relative_l2_median": float(np.median(relative)), **matching_audit})
            averaged = np.mean(matrices, axis=0)
            observed, probability, null = native_null_test(averaged, SEED, PERMUTATIONS)
            lower, upper = identity_interval(np.diag(averaged))
            means[arm] = np.diag(averaged)
            tables["native_norm_controls"].append({**common, "arm": arm, "scheme": "PolyProtect", "key_seeds": 3,
                "chance": 1 / len(averaged), "top1": observed, "lower95": lower, "upper95": upper,
                "permutation_p": probability, "null_mean": float(null.mean()),
                "linear_only_top1": float(np.mean([np.diag(matrix).mean() for matrix in linear_matrices]))})
        for comparison in ("unit", "norm_shuffled"):
            difference = means["raw"] - means[comparison]
            lower, upper = identity_interval(difference)
            tables["paired_norm_contrasts"].append({**common, "contrast": f"raw_minus_{comparison}",
                "gain": float(difference.mean()), "lower95": lower, "upper95": upper, "signflip_p": signflip(difference)})
        gallery, probes, labels = gallery_protocol(test_records)
        log_norm = np.log(norms[test_indices])
        confusion = confusion_from_scores(-np.abs(log_norm[probes, None] - log_norm[gallery][None, :]), labels)
        observed, probability, _ = native_null_test(confusion, SEED, PERMUTATIONS)
        lower, upper = identity_interval(np.diag(confusion))
        tables["norm_only_linkage"].append({**common, "chance": 1 / len(gallery), "top1": observed,
            "lower95": lower, "upper95": upper, "permutation_p": probability,
            "interpretation": "raw source norm oracle, not protected-template attack"})
        sample = test_indices[:32]
        iom_config = IoMGRPConfig()
        original_codes = iomgrp_batch(unit[sample], 91907, iom_config)
        raw_codes = iomgrp_batch(raw[sample], 91907, iom_config)
        tables["scale_invariance"].append({**common, "scheme": "IoM-GRP", "records": len(sample),
            "changed_codes": int(np.sum(original_codes != raw_codes)), "total_codes": original_codes.size})
        print(f"Native and norm controls complete: {dataset} / {split_seed}", flush=True)


def failure_analysis(destination: Path) -> None:
    rows = []
    for path in sorted((ROOT / "results/scheme_followup_2026-09-18").rglob("metrics.json")):
        result = json.loads(path.read_text())
        cell = yaml.safe_load((path.parent / "run_config.yaml").read_text())
        for condition, values in result["conditions"].items():
            baseline = {run["seed"]: run["identity_top1_scores"]
                        for run in values["exposures"]["1"]["models"]["single_mlp"]["runs"]}
            identities = sorted(next(iter(baseline.values())))
            for model, endpoint in values["exposures"]["10"]["models"].items():
                runs = sorted(endpoint["runs"], key=lambda value: value["seed"])
                if any(set(run["identity_top1_scores"]) != set(identities) for run in runs):
                    raise ValueError("Paired identity mismatch")
                differences = np.asarray([[run["identity_top1_scores"][identity] - baseline[run["seed"]][identity]
                                           for identity in identities] for run in runs])
                lower, upper = crossed_interval(differences, SEED, RESAMPLES)
                seed_gains = differences.mean(axis=1)
                rows.append({"dataset": result["dataset"], "scheme": cell["scheme_label"],
                    "split_seed": result["split_reassignment_seed"], "condition": condition, "model": model,
                    "gain": float(differences.mean()), "lower95": lower, "upper95": upper,
                    "seed_gain_min": float(seed_gains.min()), "seed_gain_max": float(seed_gains.max()),
                    "leave_one_seed_out_min": float(min(np.delete(seed_gains, index).mean() for index in range(len(runs)))),
                    "identities_with_positive_mean_gain": int((differences.mean(axis=0) > 0).sum()),
                    "identity_clusters": len(identities), "signflip_p": signflip(differences.mean(axis=0)),
                    "analysis": "post_hoc_two_sided_family_48; original_primary_unchanged"})
    if len(rows) != 48:
        raise ValueError(f"Expected 48 paired contrasts, found {len(rows)}")
    for row, probability in zip(rows, holm_adjust([row["signflip_p"] for row in rows], 48)):
        row["holm_p"] = probability
    write_table(destination / "failure_analysis.csv", rows)


def execute() -> None:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    PRIVATE.mkdir(parents=True, exist_ok=True)
    manifest_path = DESTINATION / "execution_manifest.json"
    if manifest_path.exists():
        raise FileExistsError("Existing audit freeze will not be overwritten")
    sources = [Path(__file__), ROOT / "docs/protocols/norm_native_audit_2026-09-18.md",
               ROOT / "configs/attacks/scheme_followup_2026-09-18.yaml"]
    sources += list((ROOT / "src/biometrics_ai").rglob("*.py")) + list((ROOT / "scripts/train").glob("*.py"))
    manifest = {"started_utc": datetime.now(timezone.utc).isoformat(), "budget_seconds": 3600,
                "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "dirty_worktree": bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)),
                "source_sha256": {path.relative_to(ROOT).as_posix(): digest(path) for path in sources},
                "analysis_seed": SEED, "permutations": PERMUTATIONS, "bootstrap_resamples": RESAMPLES}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    started = time.monotonic()
    tables = {name: [] for name in ("extraction_audit", "implementation_audit", "native_norm_controls",
              "paired_norm_contrasts", "norm_only_linkage", "scale_invariance")}
    config = yaml.safe_load((ROOT / "configs/attacks/scheme_followup_2026-09-18.yaml").read_text())
    datasets = {item["name"]: item for item in config["datasets"]}
    try:
        for dataset in datasets.values():
            raw, unit, metadata, audit = extract_raw(dataset, started + 3300)
            tables["extraction_audit"].append(audit)
            evaluate_dataset(dataset["name"], raw, unit, metadata, started + 3500, tables)
        for name, field, family in (("native_norm_controls", "permutation_p", 16),
                                    ("norm_only_linkage", "permutation_p", 4),
                                    ("paired_norm_contrasts", "signflip_p", 8)):
            for row, probability in zip(tables[name], holm_adjust([row[field] for row in tables[name]], family)):
                row["holm_p"] = probability
        failure_analysis(DESTINATION)
        check_deadline(started + 3600)
        manifest["status"] = "completed"
    except Exception:
        manifest["status"] = "failed_or_incomplete"
        raise
    finally:
        for name, rows in tables.items():
            if rows:
                write_table(DESTINATION / f"{name}.csv", rows)
        manifest["wall_seconds"] = round(time.monotonic() - started, 3)
        manifest["finished_utc"] = datetime.now(timezone.utc).isoformat()
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        print("Audit status:", manifest["status"], "seconds:", manifest["wall_seconds"], flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--failure-analysis-only", action="store_true")
    args = parser.parse_args()
    if args.failure_analysis_only:
        failure_analysis(DESTINATION)
    else:
        execute()