import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
STUDY = ROOT / "experiments/utility_failure_diagnostics_2026-09-26"


def test_utility_diagnostic_outputs_are_compact_and_preserved():
    summary = json.loads((STUDY / "summary.json").read_text())
    assert summary["status"] == "completed"
    assert summary["variability_cells"] == 4
    assert summary["scface_capture_cells"] == 48
    assert summary["split_overlap"] == {
        "MOBIO": {"test_identities_per_split": 30, "overlap": 7},
        "SCface": {"test_identities_per_split": 26, "overlap": 2},
    }
    with (STUDY / "variability.csv").open(newline="", encoding="utf-8") as handle:
        variability = list(csv.DictReader(handle))
    with (STUDY / "scface_capture.csv").open(newline="", encoding="utf-8") as handle:
        captures = list(csv.DictReader(handle))
    assert len(variability) == 4
    assert len(captures) == 48
    assert "identity_id" not in variability[0]
    assert "identity_id" not in captures[0]
    distance = [row for row in captures if row["aggregation"] == "distance"]
    assert len(distance) == 6
    assert all(float(row["candidate_tar"]) < 0.11 for row in distance if row["distance"] == "1")
    assert all(float(row["candidate_tar"]) > 0.50 for row in distance if row["distance"] == "3")


def test_utility_diagnostic_manifest_matches_source_and_exports_no_private_rows():
    manifest = json.loads((STUDY / "execution_manifest.json").read_text())
    source = ROOT / "scripts/diagnostics/analyse_utility_failure.py"
    assert manifest["source_sha256"] == hashlib.sha256(source.read_bytes()).hexdigest()
    assert manifest["private_files_read"] == 96
    assert manifest["private_identity_rows_exported"] == 0
