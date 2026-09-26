import csv
import json
from pathlib import Path

from scripts.diagnostics.source_provenance import verify_source

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/source_real_integration_2026-09-25"


def digest(path):
    expected = json.loads((STUDY / "execution_manifest.json").read_text())["source_sha256"]
    snapshot = (ROOT / "experiments/source_branch_fix_2026-09-26/executed_source_analysis_v2.zip",
                "source_analysis_v2.py") if path.name == "source_analysis_v2.py" else None
    return verify_source(path, expected.values(), snapshot)["sha256"]


def test_real_integration_results_and_comparison_are_preserved():
    summary = json.loads((STUDY / "summary.json").read_text())
    assert summary["cases"] == 26
    assert summary["groups"] == {"executable_recipe": 6, "frozen_confirmation": 20}
    assert summary["v3"] == {
        "decided": 25, "abstained": 1, "correct_decisions": 25,
        "false_fresh": 0, "false_reuse": 0,
        "coverage": 25 / 26, "selective_accuracy": 1,
    }
    assert summary["baseline"] == {
        "decided": 6, "abstained": 20, "correct_decisions": 5,
        "false_fresh": 0, "false_reuse": 1,
        "coverage": 6 / 26, "selective_accuracy": 5 / 6,
    }
    assert summary["v3_all_gates_pass"]
    with (STUDY / "results.csv").open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    recipes = [row for row in rows if row["group"] == "executable_recipe"]
    assert len(recipes) == 6
    assert all(row["v3_outcome"] == "correct" for row in recipes)
    assert all(row["baseline_outcome"] == "abstain" for row in recipes)


def test_real_integration_manifest_preserves_sources():
    manifest = json.loads((STUDY / "execution_manifest.json").read_text())
    assert manifest["source_sha256"] == {
        "v3": digest(ROOT / "src/biometrics_ai/protection/source_analysis_v3.py"),
        "v2": digest(ROOT / "src/biometrics_ai/protection/source_analysis_v2.py"),
        "baseline": digest(ROOT / "src/biometrics_ai/protection/syntactic_baseline.py"),
        "recipes": digest(ROOT / "scripts/diagnostics/protection_policy_recipes.py"),
        "confirmation_cases": digest(ROOT / "scripts/diagnostics/source_holdout_v2_confirmation_cases.py"),
        "evaluator": digest(ROOT / "scripts/diagnostics/evaluate_real_source_integration.py"),
        "protocol": digest(STUDY / "protocol.md"),
    }
