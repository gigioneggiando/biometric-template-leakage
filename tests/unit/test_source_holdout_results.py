import csv
import hashlib
import json
from pathlib import Path

from scripts.diagnostics.source_holdout_cases import CASES
from scripts.diagnostics.source_provenance import verify_source


ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/source_holdout_2026-09-25"


def digest(path):
    expected = json.loads((STUDY / "execution_manifest.json").read_text())["source_sha256"]
    return verify_source(path, expected.values())["sha256"]


def test_frozen_holdout_results_and_gates_are_preserved():
    summary = json.loads((STUDY / "summary.json").read_text())
    assert summary["cases"] == 24
    assert summary["labels"] == {"reuse": 12, "fresh": 12}
    assert summary["decided"] == summary["correct_decisions"] == 16
    assert summary["abstained"] == 8
    assert summary["false_fresh"] == summary["false_reuse"] == 0
    assert summary["safety_gate_pass"]
    assert summary["accuracy_gate_pass"]
    assert not summary["coverage_gate_pass"]
    assert not summary["all_gates_pass"]

    with (STUDY / "results.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 24
    assert sum(row["outcome"] == "correct" for row in rows) == 16
    assert sum(row["outcome"] == "abstain" for row in rows) == 8


def test_holdout_manifest_preserves_executed_inputs():
    manifest = json.loads((STUDY / "execution_manifest.json").read_text())
    assert manifest["status"] == "completed"
    assert manifest["source_sha256"] == {
        "analyzer": digest(ROOT / "src/biometrics_ai/protection/source_analysis.py"),
        "cases": digest(ROOT / "scripts/diagnostics/source_holdout_cases.py"),
        "evaluator": digest(ROOT / "scripts/diagnostics/evaluate_source_holdout.py"),
        "protocol": digest(STUDY / "protocol.md"),
    }
    assert manifest["case_source_sha256"] == {
        case["case"]: hashlib.sha256(case["source"].encode("utf-8")).hexdigest() for case in CASES
    }
