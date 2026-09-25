"""Evaluate v3 and an intraprocedural baseline on executable protection recipes."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
import sys
import time


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from biometrics_ai.protection.source_analysis_v3 import analyse_source_v3
from biometrics_ai.protection.syntactic_baseline import analyse_syntax
from scripts.diagnostics.source_holdout_v2_confirmation_cases import CASES


STUDY = ROOT / "experiments/source_real_integration_2026-09-25"
RECIPE_PATH = ROOT / "scripts/diagnostics/protection_policy_recipes.py"
ENTRIES = [
    "biohash_recurring", "biohash_fresh", "iomgrp_recurring", "iomgrp_fresh",
    "polyprotect_recurring", "polyprotect_fresh",
]
OUTPUTS = ("results.csv", "details.json", "summary.json", "execution_manifest.json")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metrics(rows: list[dict], prefix: str) -> dict:
    decided = sum(row[f"{prefix}_prediction"] != "abstain" for row in rows)
    correct = sum(row[f"{prefix}_outcome"] == "correct" for row in rows)
    false_fresh = sum(row[f"{prefix}_outcome"] == "false_fresh" for row in rows)
    false_reuse = sum(row[f"{prefix}_outcome"] == "false_reuse" for row in rows)
    return {
        "decided": decided,
        "abstained": len(rows) - decided,
        "correct_decisions": correct,
        "false_fresh": false_fresh,
        "false_reuse": false_reuse,
        "coverage": decided / len(rows),
        "selective_accuracy": correct / decided if decided else 0.0,
    }


def evaluate(destination: Path = STUDY) -> dict:
    existing = [name for name in OUTPUTS if (destination / name).exists()]
    if existing:
        raise FileExistsError(f"Integration outputs already exist: {', '.join(existing)}")
    recipe_source = RECIPE_PATH.read_text(encoding="utf-8")
    corpus = [
        {"case": entry, "group": "executable_recipe", "label": "reuse" if entry.endswith("recurring") else "fresh",
         "source": recipe_source, "entry": entry}
        for entry in ENTRIES
    ] + [
        {"case": case["case"], "group": "frozen_confirmation", "label": case["label"],
         "source": case["source"], "entry": "implementation"}
        for case in CASES
    ]
    started = time.perf_counter()
    rows, details = [], []
    for case in corpus:
        analyses = {
            "v3": analyse_source_v3(case["source"], case["entry"]),
            "baseline": analyse_syntax(case["source"], case["entry"]),
        }
        row = {key: case[key] for key in ("case", "group", "label")}
        for name, analysis in analyses.items():
            prediction = {"reuse": "reuse", "conditional_fresh": "fresh", "unknown": "abstain"}[
                analysis["decision"]
            ]
            outcome = (
                "abstain" if prediction == "abstain" else
                "correct" if prediction == case["label"] else
                "false_fresh" if prediction == "fresh" else "false_reuse"
            )
            row[f"{name}_prediction"] = prediction
            row[f"{name}_outcome"] = outcome
        rows.append(row)
        details.append({**row, "analyses": analyses})
    summary = {
        "status": "completed",
        "scope": "executable repository integration recipes plus frozen internal confirmation corpus",
        "cases": len(rows),
        "groups": {group: sum(row["group"] == group for row in rows) for group in {row["group"] for row in rows}},
        "v3": metrics(rows, "v3"),
        "baseline": metrics(rows, "baseline"),
        "v3_targets": {"false_fresh": 0, "selective_accuracy_min": 0.95, "coverage_min": 0.75},
    }
    summary["v3_all_gates_pass"] = (
        summary["v3"]["false_fresh"] == 0
        and summary["v3"]["selective_accuracy"] >= 0.95
        and summary["v3"]["coverage"] >= 0.75
    )
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / "results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (destination / "details.json").write_text(json.dumps(details, indent=2) + "\n", encoding="utf-8")
    (destination / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    manifest = {
        "status": "completed",
        "wall_seconds": time.perf_counter() - started,
        "source_sha256": {
            "v3": digest(ROOT / "src/biometrics_ai/protection/source_analysis_v3.py"),
            "v2": digest(ROOT / "src/biometrics_ai/protection/source_analysis_v2.py"),
            "baseline": digest(ROOT / "src/biometrics_ai/protection/syntactic_baseline.py"),
            "recipes": digest(RECIPE_PATH),
            "confirmation_cases": digest(ROOT / "scripts/diagnostics/source_holdout_v2_confirmation_cases.py"),
            "evaluator": digest(Path(__file__)),
            "protocol": digest(destination / "protocol.md"),
        },
    }
    (destination / "execution_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
