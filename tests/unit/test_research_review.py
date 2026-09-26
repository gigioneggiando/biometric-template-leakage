import pytest

from scripts.train.run_utility_replication import SEEDS, compare


def records(rate):
    return [{"master_seed": seed, "utility": {"identities": ["first", "second"],
             "identity_tar": [rate, rate], "identity_fmr": [.01, .01]}} for seed in SEEDS]


def test_fixed_replication_gate_retains_margin_and_all_seeds():
    result = compare(records(.96), records(.95))
    assert result["utility_pass"]
    assert result["tar_lower"] == pytest.approx(-.01)
    assert result["tail_alpha"] == .05 / 8
    assert not compare(records(.96), records(.92))["utility_pass"]
    with pytest.raises(ValueError, match="twelve"):
        compare(records(.96)[:-1], records(.95))


def test_replication_requires_paired_identity_order():
    after = records(.96)
    after[0]["utility"]["identities"].reverse()
    with pytest.raises(ValueError, match="identities"):
        compare(records(.96), after)


def test_review_packet_withholds_predictions_and_rejects_blank_labels(tmp_path):
    import hashlib
    import zipfile
    from scripts.diagnostics.prepare_independent_review import build_packet, validate_labels

    destination = tmp_path / "review"
    manifest = build_packet(destination, tmp_path / "coordinator")
    assert manifest["independent_labels_received"] == 0
    with zipfile.ZipFile(destination / "independent_cases.zip") as archive:
        assert len([name for name in archive.namelist() if name.endswith(".py")]) == 24
        assert not any("bandit" in name or "summary" in name or "mapping" in name for name in archive.namelist())
        labels = archive.read("labels.csv").decode()
        assert "source_decision" not in labels and "oracle" not in labels
        expected = {name.removeprefix("cases/").removesuffix(".py"): hashlib.sha256(archive.read(name)).hexdigest()
                    for name in archive.namelist() if name.endswith(".py")}
        with pytest.raises(ValueError, match="External reviewer"):
            validate_labels(labels, expected)
        for name, digest in manifest["members_sha256"].items():
            assert hashlib.sha256(archive.read(name)).hexdigest() == digest


def test_pizza_report_ascii_layout_and_render(tmp_path):
    import matplotlib.pyplot as plt
    import numpy as np
    import pypdfium2 as pdfium
    from matplotlib.text import Text
    from scripts.figures.make_pizza_algorithm_report import build_report, report_pages

    figures = report_pages()
    assert len(figures) == 9
    for figure in figures:
        figure.canvas.draw()
        renderer = figure.canvas.get_renderer()
        bounds = figure.bbox
        for text in figure.findobj(Text):
            if not text.get_visible() or not text.get_text():
                continue
            assert text.get_text().isascii()
            box = text.get_window_extent(renderer)
            assert box.x0 >= 0 and box.y0 >= 0
            assert box.x1 <= bounds.x1 and box.y1 <= bounds.y1
        boxes = [text.get_window_extent(renderer) for text in figure.texts]
        assert all(not first.overlaps(second) for index, first in enumerate(boxes) for second in boxes[index + 1:])
        plt.close(figure)
    destination = build_report(tmp_path / "pizza.pdf")
    with pdfium.PdfDocument(destination) as document:
        assert len(document) == 9
        text_parts = []
        for page in document:
            text_parts.append(page.get_textpage().get_text_range())
            image = np.asarray(page.render(scale=1).to_pil())
            assert image.std() > 10
        text = "\n".join(text_parts)
        assert "\u2014" not in text and "\u2013" not in text
        assert "2 of 4" in text and "independently certified" in text
        assert "No new participants added" in text
        assert "PROTOCOL PREPARED ONLY" in text
        assert "same 200 test people" in text
        normalized_text = " ".join(text.split())
        assert "69 historical case evaluations" in normalized_text
        assert "0 of 4 cells" in normalized_text


def test_replication_artifact_counts_gates_and_frozen_hashes():
    import csv
    import hashlib
    import json
    from scripts.train.run_utility_replication import ROOT, STUDY

    manifest = json.loads((STUDY / "execution_manifest.json").read_text())
    assert manifest["status"] == "completed"
    with (STUDY / "endpoints.csv").open(newline="") as handle:
        assert len(list(csv.DictReader(handle))) == 96
    with (STUDY / "effects.csv").open(newline="") as handle:
        effects = list(csv.DictReader(handle))
    assert len(effects) == 4
    for row in effects:
        expected = float(row["tar_lower"]) >= -.03 and float(row["fmr_upper"]) <= .02
        assert (row["utility_pass"] == "True") == expected
        assert (row["utility_pass"] == "True") == (row["dataset"] == "MOBIO")
    for path, digest in manifest["source_sha256"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest


def test_new_participant_audit_rejects_reused_and_unverified_people():
    from scripts.diagnostics.audit_new_participants import participant_overlap

    prior = [{"identity_id": "old", "split": "train"}] * 11
    reshuffled = [{"identity_id": "old", "split": "test"}] * 20
    result = participant_overlap(reshuffled, prior)
    assert result["status"] == "blocked_no_new_ids"
    assert result["previously_seen_participants"] == 1
    assert result["eligible_not_seen_by_id"] == 0
    renamed = [{"identity_id": "different_label"}] * 11
    result = participant_overlap(renamed, prior)
    assert result["eligible_not_seen_by_id"] == 1
    assert result["new_participants_verified"] == 0
    assert result["status"] == "blocked_requires_independent_identity_and_access_review"
    assert participant_overlap(renamed[:10], prior)["eligible_not_seen_by_id"] == 0
    with pytest.raises(ValueError, match="stable identity"):
        participant_overlap([{"identity_id": ""}], prior)


def test_local_cohort_audit_preserves_blocker_and_actual_algorithm_traces():
    import hashlib
    import json
    import re
    from scripts.diagnostics.audit_new_participants import ROOT
    from biometrics_ai.protection.source_analysis import analyse_source

    audit = json.loads((ROOT / "experiments/new_participant_joint_2026-09-25/cohort_audit.json").read_text())
    assert audit["status"] == "blocked_pending_new_authorized_participants"
    assert audit["new_experiment_run"] is False
    assert {row["dataset"]: row["participants"] for row in audit["cohorts"]} == {"FEI": 200, "MOBIO": 150}
    for row in audit["cohorts"]:
        assert row["eligible_not_seen_by_id"] == 0
        assert row["new_participants_verified"] == 0
        metadata_path = ROOT / row["metadata_path"]
        assert re.fullmatch(r"[0-9a-f]{64}", row["metadata_sha256"])
        if metadata_path.exists():
            assert hashlib.sha256(metadata_path.read_bytes()).hexdigest() == row["metadata_sha256"]
    source = (ROOT / "scripts/diagnostics/source_policy_recipes.py").read_text()
    for recipe, trace in audit["source_analysis"].items():
        assert json.loads(json.dumps(analyse_source(source, recipe))) == trace
    for path, key in [("scripts/diagnostics/audit_new_participants.py", "audit_source_sha256"),
                      ("scripts/diagnostics/source_policy_recipes.py", "recipe_sha256"),
                      ("src/biometrics_ai/protection/source_analysis.py", "analyzer_sha256")]:
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == audit[key]
