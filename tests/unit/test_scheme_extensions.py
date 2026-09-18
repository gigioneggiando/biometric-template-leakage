import numpy as np
import pytest
import json
from pathlib import Path
import yaml

from biometrics_ai.protection import iomgrp as iom_module
from biometrics_ai.protection.iomgrp import IoMGRPConfig, iomgrp, iomgrp_batch, iomgrp_encoded
from biometrics_ai.protection.polyprotect import PolyProtectConfig, polyprotect, polyprotect_batch, polyprotect_parameters, polyprotect_with_parameters


def test_iom_hand_computed_argmax_and_one_hot(monkeypatch):
    config = IoMGRPConfig(input_dim=2, groups=2, group_size=3)
    matrix = np.array([[1, 2, 0, 4, 2, 1], [0, 0, 3, 0, 1, 6]], dtype=np.float32)
    monkeypatch.setattr(iom_module, "_projection_matrix", lambda key, config: matrix)
    np.testing.assert_array_equal(iomgrp(np.array([1, 1]), 1, config), [2, 2])
    np.testing.assert_array_equal(iomgrp_encoded(np.array([1, 1]), 1, config), [0, 0, 1, 0, 0, 1])
    np.testing.assert_array_equal(iomgrp(np.zeros(2), 1, config), [0, 0])


def test_iom_determinism_batch_keys_and_scale():
    config = IoMGRPConfig(8, 30, 4)
    values = np.random.default_rng(7).normal(size=(12, 8))
    first = iomgrp_batch(values, 11, config)
    np.testing.assert_array_equal(first, iomgrp_batch(values, 11, config))
    np.testing.assert_array_equal(first, np.stack([iomgrp(row, 11, config) for row in values]))
    np.testing.assert_array_equal(first, iomgrp_batch(2 * values, 11, config))
    assert not np.array_equal(first, iomgrp_batch(values, 12, config))
    assert set(first.ravel()) == set(range(4))


def test_polyprotect_hand_computed_windows_and_padding():
    config = PolyProtectConfig(input_dim=6, window_size=3, overlap=1)
    actual = polyprotect_with_parameters(np.array([1, 2, 3, 4, 5, 6]), np.array([1, -2, 3]), np.array([1, 2, 3]), config)
    np.testing.assert_array_equal(actual, [1 - 2 * 4 + 3 * 27, 3 - 2 * 16 + 3 * 125, 5 - 2 * 36])


@pytest.mark.parametrize("overlap, expected", [(0, 26), (1, 32), (2, 42), (3, 63), (4, 124)])
def test_polyprotect_matches_paper_dimension_table(overlap, expected):
    config = PolyProtectConfig(input_dim=128, overlap=overlap)
    assert config.output_dim == expected
    assert polyprotect(np.ones(128), 3, config).shape == (expected,)


def test_polyprotect_determinism_parameters_and_batch():
    config = PolyProtectConfig()
    values = np.random.default_rng(7).normal(0, 0.04, (3, 512))
    coefficients, exponents = polyprotect_parameters(11, config)
    assert len(set(coefficients)) == 5 and 0 not in coefficients
    np.testing.assert_array_equal(np.sort(exponents), np.arange(1, 6))
    first = polyprotect_batch(values, 11, config)
    assert first.shape == (3, 170)
    np.testing.assert_array_equal(first, polyprotect_batch(values, 11, config))
    np.testing.assert_array_equal(first, np.stack([polyprotect(row, 11, config) for row in values]))
    assert not np.array_equal(first, polyprotect_batch(values, 12, config))
    assert np.isfinite(first).all()


@pytest.mark.parametrize("overlap", range(5))
@pytest.mark.parametrize("scale", [0.04, 1.0, 4.0])
def test_polyprotect_separate_scalar_reference(overlap, scale):
    config = PolyProtectConfig(input_dim=17, overlap=overlap)
    values = np.random.default_rng(91901).normal(size=(4, 17)) * scale
    coefficients = np.array([-43, 7, 19, -2, 50])
    exponents = np.array([3, 1, 5, 2, 4])
    reference = []
    for vector in values:
        output, offset = [], 0
        while True:
            output.append(sum(float(coefficients[position]) *
                              (float(vector[offset + position]) if offset + position < len(vector) else 0.0)
                              ** int(exponents[position]) for position in range(5)))
            if offset + 5 >= len(vector):
                break
            offset += 5 - overlap
        reference.append(output)
    actual = polyprotect_with_parameters(values, coefficients, exponents, config)
    np.testing.assert_allclose(actual, np.asarray(reference, dtype=np.float32), rtol=2e-6, atol=1e-6)


def test_iom_separate_grouped_dot_reference(monkeypatch):
    config = IoMGRPConfig(input_dim=9, groups=7, group_size=4)
    rng = np.random.default_rng(91901)
    matrix = rng.normal(size=(9, 28)).astype(np.float32)
    values = rng.normal(size=(6, 9)).astype(np.float32)
    monkeypatch.setattr(iom_module, "_projection_matrix", lambda key, config: matrix)
    reference = [[max(range(4), key=lambda category: sum(float(vector[dimension]) *
                  float(matrix[dimension, group * 4 + category]) for dimension in range(9)))
                  for group in range(7)] for vector in values]
    np.testing.assert_array_equal(iomgrp_batch(values, 1, config), reference)


def test_norm_audit_reference_matching_and_identity_protocol():
    from scripts.diagnostics.run_norm_native_audit import scalar_polyprotect, native_confusion, gallery_protocol, identity_interval, signflip

    config = PolyProtectConfig(input_dim=17)
    vector = np.random.default_rng(9).normal(size=17)
    coefficients, exponents = polyprotect_parameters(13, config)
    full, linear = scalar_polyprotect(vector, coefficients, exponents)
    np.testing.assert_allclose(full, polyprotect_with_parameters(vector, coefficients, exponents, config))
    assert linear.shape == full.shape
    metadata = [{"sample_id": f"record-{identity}-{sample}", "identity_id": str(identity), "sample_index": sample}
                for identity in range(3) for sample in range(3)]
    templates = np.repeat(np.eye(3), 3, axis=0)
    confusion, audit = native_confusion(templates, metadata)
    np.testing.assert_array_equal(confusion, np.eye(3))
    assert audit["gallery_probe_overlap"] == audit["gallery_order_disagreements"] == audit["matcher_prediction_disagreements"] == 0
    assert identity_interval(np.full(5, 0.25)) == pytest.approx((0.25, 0.25))
    assert signflip(np.zeros(6)) == 1
    with pytest.raises(ValueError, match="Duplicate"):
        gallery_protocol(metadata + [metadata[0]])


@pytest.mark.parametrize("factory", [lambda: IoMGRPConfig(group_size=1), lambda: PolyProtectConfig(overlap=5), lambda: PolyProtectConfig(coefficient_bound=1)])
def test_invalid_scheme_parameters_rejected(factory):
    with pytest.raises(ValueError):
        factory()


def test_nonfinite_input_rejected():
    for transform in (iomgrp, polyprotect):
        with pytest.raises(ValueError):
            transform(np.full(512, np.nan), 7)


def test_followup_statistics_preserve_clusters_and_family_size():
    from scripts.train.run_scheme_followup import crossed_interval, holm_adjust, native_null_test

    np.testing.assert_allclose(holm_adjust([0.01, 0.04, 0.03], 3), [0.03, 0.06, 0.06])
    np.testing.assert_allclose(holm_adjust([0.01], 8), [0.08])
    assert holm_adjust([], 8) == []
    assert crossed_interval(np.full((3, 10), 0.2), 7, 100) == pytest.approx((0.2, 0.2))
    observed, probability, null = native_null_test(np.full((8, 8), 1 / 8), 7, 99)
    assert observed == 1 / 8 and probability == 1
    np.testing.assert_allclose(null, 1 / 8)
    observed, probability, _ = native_null_test(np.eye(8), 7, 999)
    assert observed == 1 and probability < 0.01
    with pytest.raises(ValueError):
        native_null_test(np.zeros((3, 3)), 7, 99)
    with pytest.raises(ValueError):
        crossed_interval(np.zeros((1, 4)), 7, 100)


def test_followup_exports_are_complete_and_consistent():
    import csv
    from scripts.train.run_scheme_followup import holm_adjust

    root = Path(__file__).resolve().parents[2] / "experiments/scheme_followup_2026-09-18"
    def table(name):
        with (root / name).open(newline="", encoding="utf-8") as handle:
            return list(csv.DictReader(handle))

    runs = table("results_summary.csv")
    assert len(runs) == 216
    assert {row["stage"] for row in runs} == {"bounded_validation"}
    assert {int(row["seed"]) for row in runs} == {601, 607, 613}
    assert {int(row["split_seed"]) for row in runs} == {91831, 91843}
    keys = [(row["dataset"], row["scheme"], row["split_seed"], row["condition"], row["exposures"], row["model"], row["seed"]) for row in runs]
    assert len(set(keys)) == 216
    assert all(0 <= float(row["top1"]) <= 1 for row in runs)
    endpoints = table("seed_identity_endpoints.csv")
    assert len(endpoints) == 72
    for endpoint in endpoints:
        selected = [row for row in runs if all(row[key] == endpoint[key] for key in
                    ("dataset", "scheme", "split_seed", "condition", "exposures", "model"))]
        assert len(selected) == 3
        assert float(endpoint["top1_mean"]) == pytest.approx(np.mean([float(row["top1"]) for row in selected]))
    paired = table("paired_uncertainty.csv")
    assert {int(row["seed"]) for row in paired} == {601, 607, 613}
    assert {int(row["bootstrap_seed"]) for row in paired} == {91223}
    primary = [row for row in table("seed_identity_contrasts.csv") if row["primary"] == "True"]
    assert len(primary) == 8
    np.testing.assert_allclose([float(row["holm_p"]) for row in primary], holm_adjust([float(row["signflip_p"]) for row in primary], 8))
    native = table("native_null_controls.csv")
    assert len(native) == 12
    np.testing.assert_allclose([float(row["holm_p"]) for row in native], holm_adjust([float(row["permutation_p"]) for row in native], 12))
    assert len(table("norm_sensitivity.csv")) == 16
    status = json.loads((root / "matrix_status.json").read_text())
    manifest = json.loads((root / "execution_manifest.json").read_text())
    assert status["all_cells_complete"] and status["completed_cells"] == 24
    assert manifest["status"] == "completed" and manifest["wall_seconds"] < manifest["budget_seconds"]


def test_norm_audit_exports_preserve_families_and_reference_agreement():
    import pandas as pd
    from scripts.train.run_scheme_followup import holm_adjust

    root = Path(__file__).resolve().parents[2] / "experiments/norm_native_audit_2026-09-18"
    extraction = pd.read_csv(root / "extraction_audit.csv")
    assert extraction["records"].sum() == 4177
    assert (extraction["normalization_max_abs_error"] < 1e-4).all()
    audit = pd.read_csv(root / "implementation_audit.csv")
    assert len(audit) == 48
    assert (audit["records"] == audit["unique_keys"]).all()
    assert audit["reference_max_abs_error"].max() == 0
    assert audit["matcher_max_abs_error"].max() < 1e-10
    for column in ("matcher_prediction_disagreements", "gallery_order_disagreements", "top_score_ties", "gallery_probe_overlap"):
        assert audit[column].sum() == 0
    for name, count, probability in [("native_norm_controls", 16, "permutation_p"),
                                      ("norm_only_linkage", 4, "permutation_p"),
                                      ("paired_norm_contrasts", 8, "signflip_p"),
                                      ("failure_analysis", 48, "signflip_p")]:
        table = pd.read_csv(root / f"{name}.csv")
        assert len(table) == count
        assert (table["lower95"] <= table["upper95"]).all()
        np.testing.assert_allclose(table["holm_p"], holm_adjust(table[probability].tolist(), count))
    native = pd.read_csv(root / "native_norm_controls.csv")
    assert set(native["arm"]) == {"unit", "raw", "norm_shuffled", "fixed_radius"}
    assert native.groupby(["dataset", "split_seed"]).size().eq(4).all()
    previous = pd.read_csv(root.parent / "scheme_followup_2026-09-18/native_null_controls.csv")
    unit = native[native["arm"] == "unit"].set_index(["dataset", "split_seed"])["top1"].sort_index()
    expected = previous.groupby(["dataset", "split_seed"])["identity_balanced_top1"].mean().sort_index()
    np.testing.assert_allclose(unit, expected)
    scale = pd.read_csv(root / "scale_invariance.csv")
    assert len(scale) == 4 and scale["changed_codes"].sum() == 0
    manifest = json.loads((root / "execution_manifest.json").read_text())
    assert manifest["status"] == "completed" and manifest["wall_seconds"] < manifest["budget_seconds"]


@pytest.mark.parametrize("stage", ["pilot", "bounded_validation"])
def test_pilot_driver_exports_aggregates_and_validates_resume(tmp_path, stage):
    from scripts.train.run_scheme_extension_pilot import run_pilots

    root = Path(__file__).resolve().parents[2]
    config = yaml.safe_load((root / "configs/attacks/scheme_extension_pilot.yaml").read_text())
    input_dir = tmp_path / "inputs"
    input_dir.mkdir()
    metadata, values = [], []
    rng = np.random.default_rng(11)
    for split, identities in [("train", 3), ("val", 2), ("test", 2)]:
        for identity in range(identities):
            for sample in range(12):
                vector = rng.normal(size=512)
                values.append(vector / np.linalg.norm(vector))
                metadata.append({"identity_id": f"{split}_{identity}", "sample_id": f"{split}_{identity}_{sample}",
                                 "sample_index": sample, "split": split})
    np.save(input_dir / "embeddings.npy", np.asarray(values, dtype=np.float32))
    (input_dir / "metadata.json").write_text(json.dumps(metadata))
    (input_dir / "embedding_manifest.json").write_text("{}")
    config.update(datasets=[{"name": "fixture", "embedding_dir": str(input_dir)}],
                  schemes=[config["schemes"][1]], conditions=["independent_unseen_keys"],
                  repeats_per_identity=1, output_root=str(tmp_path / "runs"), summary_dir=str(tmp_path / "summary"))
    config["training"].update(epochs=1, patience=1, hidden_dim=4, bootstrap_resamples=10)
    config["stage"] = stage
    if stage == "bounded_validation":
        config["datasets"] = [{**config["datasets"][0], "split_reassignment_seed": seed} for seed in (11, 17)]
        config["training"]["seeds"] = [419, 421, 431]
    result = run_pilots(config)
    expected_cells = len(config["datasets"])
    assert result["all_cells_complete"] and result["completed_cells"] == expected_cells
    from scripts.figures.build_run_matrix import collect_runs
    matrix = collect_runs(tmp_path / "runs")
    assert len(matrix) == 3 * expected_cells * len(config["training"]["seeds"])
    assert {row["stage"] for row in matrix} == {stage}
    assert all(row["identity_pairing_available"] for row in matrix)
    assert all(len(row["config_sha256"]) == 64 for row in matrix)
    assert "test_0" not in json.dumps(matrix)
    legacy = tmp_path / "runs" / "legacy"
    legacy.mkdir()
    (legacy / "metrics.json").write_text(json.dumps({"split_identity_counts": {"test": 2}, "conditions": {"fresh": {"runs": []}}}))
    assert collect_runs(tmp_path / "runs") == matrix
    for filename in ["results_summary.csv", "native_utility.csv", "paired_uncertainty.csv", "equivalence_sensitivity.csv"]:
        text = (tmp_path / "summary" / filename).read_text()
        assert text.count("\n") > 1
        assert "train_0" not in text and "test_0" not in text
    import csv
    with (tmp_path / "summary" / "paired_uncertainty.csv").open() as handle:
        paired = list(csv.DictReader(handle))
    assert {int(row["seed"]) for row in paired} == set(config["training"]["seeds"])
    assert {int(row["bootstrap_seed"]) for row in paired} == {91223}
    assert len(paired) == 2 * expected_cells * len(config["training"]["seeds"])
    assert run_pilots(config, resume=True)["cells"][0]["status"] == "reused"
    with pytest.raises(FileExistsError):
        run_pilots(config)
    config["key_seed"] += 1
    with pytest.raises(ValueError, match="differs"):
        run_pilots(config, resume=True)