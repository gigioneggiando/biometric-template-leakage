import csv
import hashlib
import json
from pathlib import Path

from scripts.diagnostics.source_holdout_v2_confirmation_cases import CASES


ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/source_holdout_v2_confirmation_2026-09-25"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_v2_confirmation_results_and_gates_are_preserved():
    summary = json.loads((STUDY / "summary.json").read_text())
    assert summary["cases"] == 20
    assert summary["labels"] == {"reuse": 10, "fresh": 10}
    assert summary["decided"] == summary["correct_decisions"] == 19
    assert summary["abstained"] == 1
    assert summary["false_fresh"] == summary["false_reuse"] == 0
    assert summary["coverage"] == 0.95
    assert summary["selective_accuracy"] == 1
    assert summary["all_gates_pass"]
    with (STUDY / "results.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert [row["case"] for row in rows if row["outcome"] == "abstain"] == ["fresh_floor_identity"]


def test_v2_confirmation_manifest_preserves_executed_inputs():
    manifest = json.loads((STUDY / "execution_manifest.json").read_text())
    assert manifest["source_sha256"] == {
        "analyzer_v2": digest(ROOT / "src/biometrics_ai/protection/source_analysis_v2.py"),
        "cases": digest(ROOT / "scripts/diagnostics/source_holdout_v2_confirmation_cases.py"),
        "evaluator": digest(ROOT / "scripts/diagnostics/evaluate_source_holdout_v2_confirmation.py"),
        "protocol": digest(STUDY / "protocol.md"),
    }
    assert manifest["case_source_sha256"] == {
        case["case"]: hashlib.sha256(case["source"].encode("utf-8")).hexdigest() for case in CASES
    }
