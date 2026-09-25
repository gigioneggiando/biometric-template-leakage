"""Run source-analysis v2 once on the frozen confirmation corpus."""
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

from biometrics_ai.protection.source_analysis_v2 import analyse_source_v2
from scripts.diagnostics.source_holdout_v2_confirmation_cases import CASES


DESTINATION = ROOT / "experiments/source_holdout_v2_confirmation_2026-09-25"
OUTPUTS = ("results.csv", "details.json", "summary.json", "execution_manifest.json")


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def evaluate(destination: Path = DESTINATION) -> dict:
    existing = [name for name in OUTPUTS if (destination / name).exists()]
    if existing:
        raise FileExistsError(f"Confirmation outputs already exist: {', '.join(existing)}")
    started = time.perf_counter()
    rows, details = [], []
    for case in CASES:
        analysis = analyse_source_v2(case["source"], "implementation")
        prediction = {"reuse": "reuse", "conditional_fresh": "fresh", "unknown": "abstain"}[
            analysis["decision"]
        ]
        outcome = (
            "abstain"
            if prediction == "abstain"
            else "correct"
            if prediction == case["label"]
            else "false_fresh"
            if prediction == "fresh"
            else "false_reuse"
        )
        row = {
            "case": case["case"], "label": case["label"], "prediction": prediction,
            "outcome": outcome, "complete": analysis["complete"],
        }
        rows.append(row)
        details.append({**row, "rationale": case["rationale"], "analysis": analysis})

    decided = sum(row["prediction"] != "abstain" for row in rows)
    correct = sum(row["outcome"] == "correct" for row in rows)
    summary = {
        "status": "completed",
        "scope": "internally authored, post-implementation frozen confirmation",
        "cases": len(rows),
        "labels": {label: sum(row["label"] == label for row in rows) for label in ("reuse", "fresh")},
        "decided": decided,
        "abstained": len(rows) - decided,
        "correct_decisions": correct,
        "false_fresh": sum(row["outcome"] == "false_fresh" for row in rows),
        "false_reuse": sum(row["outcome"] == "false_reuse" for row in rows),
        "coverage": decided / len(rows),
        "selective_accuracy": correct / decided if decided else 0.0,
        "targets": {"false_fresh": 0, "selective_accuracy_min": 0.95, "coverage_min": 0.75},
    }
    summary["safety_gate_pass"] = summary["false_fresh"] == 0
    summary["accuracy_gate_pass"] = summary["selective_accuracy"] >= 0.95
    summary["coverage_gate_pass"] = summary["coverage"] >= 0.75
    summary["all_gates_pass"] = all(
        summary[name] for name in ("safety_gate_pass", "accuracy_gate_pass", "coverage_gate_pass")
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
            "analyzer_v2": digest(ROOT / "src/biometrics_ai/protection/source_analysis_v2.py"),
            "cases": digest(ROOT / "scripts/diagnostics/source_holdout_v2_confirmation_cases.py"),
            "evaluator": digest(Path(__file__)),
            "protocol": digest(destination / "protocol.md"),
        },
        "case_source_sha256": {
            case["case"]: hashlib.sha256(case["source"].encode("utf-8")).hexdigest() for case in CASES
        },
    }
    (destination / "execution_manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return summary


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
