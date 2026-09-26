import csv
import json
from pathlib import Path

import pytest

from scripts.diagnostics.source_provenance import verify_source

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
    assert verify_source(source, [manifest["source_sha256"]])["sha256"] == manifest["source_sha256"]
    assert manifest["private_files_read"] == 96
    assert manifest["private_identity_rows_exported"] == 0


def test_precision_planning_null_boundary_and_variability_axes():
    from math import sqrt
    from scripts.diagnostics.plan_utility_precision import precision_scenario

    boundary = precision_scenario(.06, .04, 200, 12, -.03)
    assert boundary["normal_approximation_tar_power"] == pytest.approx(.05 / 3)
    baseline = precision_scenario(.06, .04, 200, 12, -.01)
    assert baseline["proxy_standard_error"] == pytest.approx(sqrt(.06 ** 2 / 200 + .04 ** 2 / 12))
    assert precision_scenario(.06, .04, 400, 12, -.01)["normal_approximation_tar_power"] > baseline["normal_approximation_tar_power"]
    assert precision_scenario(.06, .04, 200, 48, -.01)["normal_approximation_tar_power"] > baseline["normal_approximation_tar_power"]
    assert precision_scenario(.06, .04, 200, 12, -.01, 2)["normal_approximation_tar_power"] < baseline["normal_approximation_tar_power"]
    assert precision_scenario(.06, .04, 10 ** 9, 12, -.01)["proxy_standard_error"] == pytest.approx(.04 / sqrt(12))


@pytest.mark.parametrize("changes", [
    {"identity_sd": float("nan")}, {"key_sd": -.1}, {"test_people": 1},
    {"key_draws": 12.5}, {"tail_alpha": 0}, {"variance_multiplier": 0},
    {"identity_sd": 0, "key_sd": 0},
])
def test_precision_planning_rejects_invalid_inputs(changes):
    from scripts.diagnostics.plan_utility_precision import precision_scenario

    inputs = dict(identity_sd=.06, key_sd=.04, test_people=200, key_draws=12, mean_change=-.01)
    with pytest.raises(ValueError):
        precision_scenario(**(inputs | changes))


def test_precision_planning_exports_aggregates_without_claiming_confirmation(tmp_path):
    import hashlib
    from scripts.diagnostics.plan_utility_precision import execute

    summary = execute(tmp_path)
    assert summary["scenarios"] == 384
    assert summary["new_participants"] == summary["new_biometric_evaluations"] == 0
    assert not summary["joint_power_established"]
    assert not summary["independent_validation_completed"]
    assert hashlib.sha256((tmp_path / "scenarios.csv").read_bytes()).hexdigest() == summary["scenarios_sha256"]
    with (tmp_path / "scenarios.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 384
    assert "identity_id" not in rows[0]
    with pytest.raises(FileExistsError, match="overwrite"):
        execute(tmp_path)


def test_saved_precision_scenarios_match_inputs_and_formula():
    import hashlib
    from scripts.diagnostics.plan_utility_precision import DESTINATION, precision_scenario

    summary = json.loads((DESTINATION / "summary.json").read_text())
    for path, digest in summary["source_sha256"].items():
        assert verify_source(ROOT / path, [digest])["sha256"] == digest
    assert hashlib.sha256((DESTINATION / "scenarios.csv").read_bytes()).hexdigest() == summary["scenarios_sha256"]
    with (DESTINATION / "scenarios.csv").open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == summary["scenarios"] == 384
    for row in rows:
        result = precision_scenario(float(row["identity_axis_sd"]), float(row["key_axis_sd"]),
                                    int(row["test_people"]), int(row["key_draws"]),
                                    float(row["assumed_mean_tar_change"]), float(row["variance_multiplier"]))
        assert float(row["normal_approximation_tar_power"]) == pytest.approx(result["normal_approximation_tar_power"])
