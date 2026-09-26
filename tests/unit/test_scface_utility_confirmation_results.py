import csv
import json
from pathlib import Path

from scripts.diagnostics.source_provenance import verify_source

ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/scface_utility_confirmation_2026-09-25"


def digest(path):
    expected = json.loads((STUDY / "execution_manifest.json").read_text())["source_sha256"]
    return verify_source(path, expected.values())["sha256"]


def test_scface_utility_confirmation_preserves_failed_gates():
    manifest = json.loads((STUDY / "execution_manifest.json").read_text())
    assert manifest["status"] == "completed"
    assert manifest["completed_evaluations"] == 96
    assert manifest["utility_passes"] == 0
    assert not manifest["scface_primary_pass"]
    assert not manifest["all_cells_pass"]
    with (STUDY / "effects.csv").open(newline="", encoding="utf-8") as handle:
        effects = list(csv.DictReader(handle))
    assert len(effects) == 4
    assert all(row["utility_pass"] == "False" for row in effects)
    assert all(float(row["fmr_upper"]) <= 0.02 for row in effects)
    assert all(float(row["tar_lower"]) < -0.03 for row in effects)
    with (STUDY / "endpoints.csv").open(newline="", encoding="utf-8") as handle:
        assert len(list(csv.DictReader(handle))) == 96


def test_scface_utility_confirmation_preserves_executed_sources():
    manifest = json.loads((STUDY / "execution_manifest.json").read_text())
    assert manifest["source_sha256"] == {
        "scripts/train/run_scface_utility_confirmation.py": digest(
            ROOT / "scripts/train/run_scface_utility_confirmation.py"
        ),
        "scripts/train/run_source_security_utility.py": digest(
            ROOT / "scripts/train/run_source_security_utility.py"
        ),
        "src/biometrics_ai/evaluation/security_utility.py": digest(
            ROOT / "src/biometrics_ai/evaluation/security_utility.py"
        ),
        "docs/protocols/scface_utility_confirmation_2026-09-25.md": digest(
            ROOT / "docs/protocols/scface_utility_confirmation_2026-09-25.md"
        ),
    }
