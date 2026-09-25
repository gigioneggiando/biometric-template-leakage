import copy

import pytest

from biometrics_ai.protection.policy import analyse_policy, recommend_fresh_policy


def policy(condition="random_key_pool_4", scheme="biohash"):
    return {"template_dim": 128, "protection": {"scheme": scheme, "haar_sign_corrected": True},
            "conditions": [condition], "training": {"seeds": [601, 607, 613]}}


@pytest.mark.parametrize("condition", ["random_key_pool_1", "random_key_pool_10000", "system_key_pool_4", "shared_key_calibration"])
def test_reuse_is_blocked_without_fitting_an_attacker(condition):
    result = analyse_policy(policy(condition))
    assert result["decision"] == "block"
    assert "KEY_REUSE" in {finding["rule"] for finding in result["findings"]}


@pytest.mark.parametrize("condition", ["correlated_key_25", "correlated_dims_1", "correlated_dims_128"])
def test_shared_projection_is_blocked(condition):
    assert "KEY_CORRELATION" in {finding["rule"] for finding in analyse_policy(policy(condition))["findings"]}


@pytest.mark.parametrize("condition", ["independent_unseen_keys", "correlated_key_0", "correlated_dims_0"])
def test_fresh_scope_never_becomes_a_security_certificate(condition):
    result = analyse_policy(policy(condition))
    assert result["decision"] == "review"
    assert result["scopes"][0]["scope"] == "fresh_declared"
    assert result["findings"][0]["rule"] == "RUNTIME_ASSUMPTIONS"


@pytest.mark.parametrize("condition", ["random_key_pool_0", "random_key_pool_-1", "correlated_key_13", "correlated_dims_129", "fresh", "random_key_pool_4\n"])
def test_unknown_or_invalid_condition_fails_closed(condition):
    assert analyse_policy(policy(condition))["decision"] == "block"
    with pytest.raises(ValueError, match="Unsupported"):
        recommend_fresh_policy(policy(condition))


def test_remediation_preserves_matched_training_and_residual_warnings():
    original = policy(scheme="polyprotect_paper_specified")
    original["protection"]["include_key_slot"] = True
    snapshot = copy.deepcopy(original)
    candidate = recommend_fresh_policy(original)
    assert original == snapshot
    assert candidate["conditions"] == ["independent_unseen_keys"]
    assert candidate["training"] == original["training"]
    assert "include_key_slot" not in candidate["protection"]
    result = analyse_policy(candidate)
    assert result["decision"] == "review"
    assert "NATIVE_LINKAGE_REVIEW" in {finding["rule"] for finding in result["findings"]}


@pytest.mark.parametrize("config", [None, {}, {"schemes": None}, {"conditions": "independent_unseen_keys"},
                                  policy(scheme="new_scheme"), {**policy(), "template_dim": True}])
def test_malformed_inputs_fail_closed(config):
    assert analyse_policy(config)["decision"] == "block"


def test_matrix_reports_each_scheme_condition():
    config = {"schemes": [{"protection": {"scheme": name}, "template_dim": 128}
                           for name in ["biohash", "polyprotect_paper_specified"]],
              "conditions": ["random_key_pool_4", "independent_unseen_keys"]}
    assert len(analyse_policy(config)["scopes"]) == 4
    assert analyse_policy(recommend_fresh_policy(config))["decision"] == "review"


@pytest.mark.parametrize("condition", ["random_key_pool_4", "system_key_pool_2", "shared_key_calibration",
                                       "independent_unseen_keys", "correlated_dims_1", "correlated_key_0"])
def test_static_scope_agrees_with_runtime_key_audit(condition):
    import numpy as np
    from scripts.train.run_real_multiexposure import protect_embeddings

    config = {**policy(condition), "template_dim": 4}
    metadata = [{"sample_id": str(index), "sample_index": index, "split": split}
                for index, split in enumerate(["train", "train", "val", "val", "test", "test"])]
    _, audit = protect_embeddings(np.eye(6), metadata, condition, 73, 4, config["protection"])
    scope = analyse_policy(config)["scopes"][0]["scope"]
    if scope == "shared_across_splits":
        assert audit["split_key_disjoint"] is False
    elif scope == "shared_projection":
        assert audit["shared_projection_dimensions"] > 0
    else:
        assert audit.get("split_key_disjoint", audit.get("split_private_keys_disjoint")) is True
        assert audit.get("shared_projection_dimensions", 0) == 0


def test_paired_effect_has_correct_direction_and_rejects_misalignment():
    from scripts.train.run_static_policy_evaluation import paired_effect

    before = {"runs": [{"seed": seed, "identity_top1_scores": {"first": 1.0, "second": 0.75}} for seed in [1, 2, 3]]}
    after = {"runs": [{"seed": seed, "identity_top1_scores": {"first": 0.25, "second": 0.0}} for seed in [1, 2, 3]]}
    analysis = {"seed": 17, "bootstrap_resamples": 99, "permutations": 99}
    result = paired_effect(before, after, analysis)
    assert result["reduction"] == result["lower95"] == result["upper95"] == 0.75
    assert result["chance"] == 0.5
    after["runs"][0]["identity_top1_scores"] = {"other": 0.0, "second": 0.0}
    with pytest.raises(ValueError, match="align"):
        paired_effect(before, after, analysis)


def test_frozen_study_preserves_sources_and_all_endpoints():
    import csv
    import hashlib
    import json
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    study = root / "experiments/static_policy_2026-09-25"
    manifest = json.loads((study / "execution_manifest.json").read_text())
    assert manifest["status"] == "completed"
    assert manifest["completed_cells"] == 16
    for relative, expected in manifest["source_sha256"].items():
        assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == expected, relative
    with (study / "results_summary.csv").open(newline="") as handle:
        endpoints = list(csv.DictReader(handle))
    assert len(endpoints) == 96
    with (study / "policy_effects.csv").open(newline="") as handle:
        effects = list(csv.DictReader(handle))
    primary = [row for row in effects if row["primary"] == "True"]
    assert len(primary) == 8
    for row in effects:
        assert float(row["reduction"]) == pytest.approx(float(row["before_top1"]) - float(row["after_top1"]))
        for condition, column in [("random_key_pool_4", "before_top1"), ("independent_unseen_keys", "after_top1")]:
            matches = [endpoint for endpoint in endpoints if all(endpoint[key] == row[key]
                       for key in ("dataset", "scheme", "split_seed", "exposures", "model")) and endpoint["condition"] == condition]
            assert len(matches) == 3
            assert float(row[column]) == pytest.approx(sum(float(endpoint["top1"]) for endpoint in matches) / 3)


def test_report_builds_three_searchable_nonblank_pages(tmp_path, monkeypatch):
    pytest.importorskip("matplotlib")
    pdfium = pytest.importorskip("pypdfium2")
    import numpy as np
    from scripts.figures import make_static_policy_report as report

    original = report.PdfPages.savefig

    def check_bounds(pdf, figure, **kwargs):
        figure.canvas.draw()
        renderer = figure.canvas.get_renderer()
        boxes = [artist.get_window_extent(renderer) for artist in figure.texts]
        for box in boxes:
            assert figure.bbox.contains(box.x0, box.y0) and figure.bbox.contains(box.x1, box.y1)
        for index, box in enumerate(boxes):
            assert not any(box.overlaps(other) for other in boxes[index + 1:])
        for axis in figure.axes:
            for artist in axis.tables:
                for cell in artist.get_celld().values():
                    text_box = cell.get_text().get_window_extent(renderer)
                    cell_box = cell.get_window_extent(renderer).padded(1)
                    assert cell_box.contains(text_box.x0, text_box.y0) and cell_box.contains(text_box.x1, text_box.y1)
        return original(pdf, figure, **kwargs)

    monkeypatch.setattr(report.PdfPages, "savefig", check_bounds)
    destination = tmp_path / "report.pdf"
    report.build_report(destination)
    with pdfium.PdfDocument(destination) as document:
        assert len(document) == 3
        for page in document:
            text_page = page.get_textpage()
            try:
                assert len(text_page.get_text_range()) > 300
            finally:
                text_page.close()
            pixels = np.asarray(page.render(scale=.7).to_pil())
            assert np.std(pixels) > 10