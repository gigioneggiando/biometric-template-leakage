import csv
import json
from pathlib import Path

from scripts.diagnostics.source_provenance import verify_source

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/source_holdout_v2_2026-09-25"


def digest(path):
    expected = json.loads((STUDY / "execution_manifest.json").read_text())["source_sha256"]
    snapshot = (ROOT / "experiments/source_branch_fix_2026-09-26/executed_source_analysis_v2.zip",
                "source_analysis_v2.py") if path.name == "source_analysis_v2.py" else None
    return verify_source(path, expected.values(), snapshot)["sha256"]


def test_v2_development_results_and_gates_are_preserved():
    summary = json.loads((STUDY / "summary.json").read_text())
    assert summary["valid_cases"] == 23
    assert summary["decided"] == summary["correct_decisions"] == 22
    assert summary["abstained"] == 1
    assert summary["false_fresh"] == summary["false_reuse"] == 0
    assert summary["coverage"] == 22 / 23
    assert summary["selective_accuracy"] == 1
    assert summary["all_gates_pass"]
    with (STUDY / "results.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 24
    assert [row["case"] for row in rows if row["outcome"] == "excluded_invalid"] == [
        "fresh_keyword_arguments"
    ]
    assert [row["case"] for row in rows if row["outcome"] == "abstain"] == [
        "fresh_equivalent_branches"
    ]


def test_v2_development_manifest_preserves_sources():
    manifest = json.loads((STUDY / "execution_manifest.json").read_text())
    assert manifest["source_sha256"] == {
        "analyzer_v1": digest(ROOT / "src/biometrics_ai/protection/source_analysis.py"),
        "analyzer_v2": digest(ROOT / "src/biometrics_ai/protection/source_analysis_v2.py"),
        "cases": digest(ROOT / "scripts/diagnostics/source_holdout_cases.py"),
        "evaluator": digest(ROOT / "scripts/diagnostics/evaluate_source_holdout_v2.py"),
    }
