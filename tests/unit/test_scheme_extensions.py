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


@pytest.mark.parametrize("factory", [lambda: IoMGRPConfig(group_size=1), lambda: PolyProtectConfig(overlap=5), lambda: PolyProtectConfig(coefficient_bound=1)])
def test_invalid_scheme_parameters_rejected(factory):
    with pytest.raises(ValueError):
        factory()


def test_nonfinite_input_rejected():
    for transform in (iomgrp, polyprotect):
        with pytest.raises(ValueError):
            transform(np.full(512, np.nan), 7)


def test_pilot_driver_exports_aggregates_and_validates_resume(tmp_path):
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
    result = run_pilots(config)
    assert result["all_cells_complete"] and result["completed_cells"] == 1
    from scripts.figures.build_run_matrix import collect_runs
    matrix = collect_runs(tmp_path / "runs")
    assert len(matrix) == 3
    assert {row["stage"] for row in matrix} == {"pilot"}
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
    assert run_pilots(config, resume=True)["cells"][0]["status"] == "reused"
    with pytest.raises(FileExistsError):
        run_pilots(config)
    config["key_seed"] += 1
    with pytest.raises(ValueError, match="differs"):
        run_pilots(config, resume=True)