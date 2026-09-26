import hashlib
import zipfile

import pytest

from scripts.diagnostics.source_provenance import verify_source


def test_checkout_conversion_requires_the_original_hash(tmp_path):
    original = b"value = 1\n"
    expected = hashlib.sha256(original).hexdigest()
    path = tmp_path / "source.py"
    path.write_bytes(original)
    assert verify_source(path, [expected])["mode"] == "checkout_exact"
    path.write_bytes(b"value = 1\r\n")
    assert verify_source(path, [expected]) == {"sha256": expected, "mode": "checkout_to_lf"}
    crlf_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    path.write_bytes(original)
    assert verify_source(path, [crlf_hash])["mode"] == "checkout_to_crlf"
    path.write_bytes(b"value = 2\r\n")
    with pytest.raises(ValueError, match="frozen manifest"):
        verify_source(path, [expected])
    with pytest.raises(ValueError, match="manifest hash"):
        verify_source(path, [])


def test_snapshot_is_explicit_and_must_match_exact_bytes(tmp_path):
    path = tmp_path / "source.py"
    path.write_bytes(b"changed = True\n")
    original = b"value = 1\n"
    expected = hashlib.sha256(original).hexdigest()
    archive_path = tmp_path / "executed.zip"
    with zipfile.ZipFile(archive_path, "w") as archive:
        archive.writestr("source.py", original)
        archive.writestr("wrong.py", original.replace(b"\n", b"\r\n"))
    with pytest.raises(ValueError):
        verify_source(path, [expected])
    assert verify_source(path, [expected], (archive_path, "source.py"))["mode"] == "snapshot_exact"
    with pytest.raises(ValueError):
        verify_source(path, [expected], (archive_path, "wrong.py"))


def test_post_fix_regression_matches_current_sources_and_frozen_predictions():
    import json
    from pathlib import Path
    from biometrics_ai.protection.source_analysis_v2 import analyse_source_v2
    from biometrics_ai.protection.source_analysis_v3 import analyse_source_v3

    root = Path(__file__).resolve().parents[2]
    result = json.loads((root / "experiments/source_branch_fix_2026-09-26/regression.json").read_text())
    assert result["case_evaluations"] == len(result["cases"]) == 69
    assert result["changed_predictions"] == result["false_fresh"] == 0
    assert all(row["current_prediction"] == row["frozen_prediction"] for row in result["cases"])
    for path, expected in result["source_and_input_sha256"].items():
        verify_source(root / path, [expected])
    counterexample = result["counterexample"]
    assert counterexample["records"] == 8 and counterexample["distinct_keys"] == 4
    for name, analyze in [("v2", analyse_source_v2), ("v3", analyse_source_v3)]:
        assert json.loads(json.dumps(analyze(counterexample["source"], "implementation"))) == counterexample[name]
        assert counterexample[name]["decision"] == "unknown"
        assert not counterexample[name]["complete"]