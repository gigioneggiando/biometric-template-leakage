"""Native-matching comparison: naive vs stricter PolyProtect parameter selection.

See docs/protocols/polyprotect_stricter_audit_2026-09-19.md, frozen before execution.
"""
from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from biometrics_ai.protection import generate_key
from biometrics_ai.protection.polyprotect import (
    PolyProtectConfig,
    polyprotect_parameters,
    polyprotect_parameters_stricter,
    polyprotect_with_parameters,
)
from scripts.train import run_real_multiexposure as runner
from scripts.train.run_scheme_extension_pilot import write_table
from scripts.train.run_scheme_followup import holm_adjust, native_null_test
from scripts.diagnostics.run_norm_native_audit import gallery_protocol, native_confusion, identity_interval, signflip

DESTINATION = ROOT / "experiments/polyprotect_stricter_audit_2026-09-19"
BUDGET_SECONDS = 1800
KEY_SEEDS = (92003, 92011, 92017)
CANDIDATES = 20
MAX_DEVELOPMENT_PAIRS = 200
DATASETS = [
    {"name": "MOBIO", "embedding_dir": "data/processed/embeddings/mobio/buffalo_l_yunet"},
    {"name": "SCface", "embedding_dir": "data/processed/embeddings/scface_multiexposure/buffalo_l_yunet"},
]


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_deadline(deadline: float) -> None:
    if time.monotonic() >= deadline:
        raise TimeoutError("Frozen audit budget exhausted")


def protect_arm(embeddings: np.ndarray, metadata: list[dict], key_seed: int, config: PolyProtectConfig, arm: str,
                deadline: float, development_embeddings: np.ndarray | None = None,
                development_ids: np.ndarray | None = None) -> np.ndarray:
    keys = [generate_key(key_seed, str(row["split"]), str(row["sample_id"])) for row in metadata]
    if len(set(keys)) != len(keys):
        raise RuntimeError("Independent key generation produced duplicate keys")
    templates = []
    for index, (embedding, key) in enumerate(zip(embeddings, keys)):
        if index % 50 == 0:
            check_deadline(deadline)
        if arm == "naive":
            coefficients, exponents = polyprotect_parameters(key, config)
        elif arm == "stricter":
            coefficients, exponents = polyprotect_parameters_stricter(
                key, development_embeddings, development_ids, config,
                candidates=CANDIDATES, max_development_pairs=MAX_DEVELOPMENT_PAIRS)
        else:
            raise ValueError(f"Unknown arm: {arm}")
        templates.append(polyprotect_with_parameters(embedding, coefficients, exponents, config))
    return np.stack(templates)


def evaluate_dataset(dataset: dict, deadline: float, tables: dict[str, list[dict]]) -> None:
    directory = ROOT / dataset["embedding_dir"]
    embeddings, metadata, manifest = runner.load_embeddings(directory)
    config = PolyProtectConfig()
    train_indices = [index for index, row in enumerate(metadata) if row["split"] == "train"]
    test_indices = np.asarray([index for index, row in enumerate(metadata) if row["split"] == "test"])
    test_records = [metadata[index] for index in test_indices]
    development_embeddings = embeddings[train_indices]
    development_ids = np.asarray([str(metadata[index]["identity_id"]) for index in train_indices])
    matrices = {"naive": [], "stricter": []}
    for key_seed in KEY_SEEDS:
        check_deadline(deadline)
        naive_templates = protect_arm(embeddings[test_indices], test_records, key_seed, config, "naive", deadline)
        stricter_templates = protect_arm(embeddings[test_indices], test_records, key_seed, config, "stricter", deadline,
                                         development_embeddings, development_ids)
        for arm, templates in (("naive", naive_templates), ("stricter", stricter_templates)):
            confusion, audit = native_confusion(templates, test_records)
            matrices[arm].append(confusion)
            tables["implementation_audit"].append({"dataset": dataset["name"], "arm": arm, "key_seed": key_seed,
                "records": len(templates), **audit})
        print(f"{dataset['name']} key seed {key_seed} complete", flush=True)
    means = {}
    for arm in ("naive", "stricter"):
        averaged = np.mean(matrices[arm], axis=0)
        observed, probability, null = native_null_test(averaged, 91903, 4999)
        lower, upper = identity_interval(np.diag(averaged))
        means[arm] = np.diag(averaged)
        tables["native_comparison"].append({"dataset": dataset["name"], "arm": arm, "key_seeds": len(KEY_SEEDS),
            "candidates": CANDIDATES, "max_development_pairs": MAX_DEVELOPMENT_PAIRS,
            "chance": 1 / len(averaged), "top1": observed, "lower95": lower, "upper95": upper,
            "permutation_p": probability, "null_mean": float(null.mean())})
    difference = means["stricter"] - means["naive"]
    lower, upper = identity_interval(difference)
    tables["paired_contrasts"].append({"dataset": dataset["name"], "contrast": "stricter_minus_naive",
        "gain": float(difference.mean()), "lower95": lower, "upper95": upper, "signflip_p": signflip(difference)})
    print(f"Native comparison complete: {dataset['name']}", flush=True)


def execute() -> None:
    DESTINATION.mkdir(parents=True, exist_ok=True)
    manifest_path = DESTINATION / "execution_manifest.json"
    if manifest_path.exists():
        raise FileExistsError("Existing audit freeze will not be overwritten")
    sources = [Path(__file__), ROOT / "docs/protocols/polyprotect_stricter_audit_2026-09-19.md",
               ROOT / "src/biometrics_ai/protection/polyprotect.py",
               ROOT / "scripts/diagnostics/run_norm_native_audit.py",
               ROOT / "scripts/train/run_real_multiexposure.py",
               ROOT / "scripts/train/run_scheme_followup.py",
               ROOT / "scripts/train/run_scheme_extension_pilot.py"]
    manifest = {"started_utc": datetime.now(timezone.utc).isoformat(), "budget_seconds": BUDGET_SECONDS,
                "base_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "dirty_worktree": bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)),
                "source_sha256": {path.relative_to(ROOT).as_posix(): digest(path) for path in sources},
                "key_seeds": list(KEY_SEEDS), "candidates": CANDIDATES,
                "max_development_pairs": MAX_DEVELOPMENT_PAIRS, "datasets": [item["name"] for item in DATASETS]}
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
    started = time.monotonic()
    deadline = started + BUDGET_SECONDS
    tables = {name: [] for name in ("implementation_audit", "native_comparison", "paired_contrasts")}
    try:
        for dataset in DATASETS:
            evaluate_dataset(dataset, deadline, tables)
        for row, probability in zip(tables["native_comparison"], holm_adjust(
                [row["permutation_p"] for row in tables["native_comparison"]], 4)):
            row["holm_p"] = probability
        for row, probability in zip(tables["paired_contrasts"], holm_adjust(
                [row["signflip_p"] for row in tables["paired_contrasts"]], 2)):
            row["holm_p"] = probability
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
    execute()
