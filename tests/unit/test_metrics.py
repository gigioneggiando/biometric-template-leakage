import numpy as np
import pytest
from biometrics_ai.evaluation.metrics import (
    eer,
    gallery_probe_metrics,
    identity_clustered_top1_interval,
    top_k_linkage,
    paired_identity_interval,
    exploratory_equivalence_sensitivity,
)


def test_metrics():
    assert eer(np.array([1, 1, 0, 0]), np.array([.9, .8, .2, .1])) < .01
    preds = np.eye(3); assert top_k_linkage(preds, preds, np.array([0, 1, 2]), 1) == 1.0


def test_gallery_probe_metrics_support_multiple_probes_per_identity():
    gallery = np.eye(2, dtype=np.float32)
    predictions = np.asarray([[1, 0], [.9, .1], [0, 1], [.1, .9]], dtype=np.float32)
    metrics = gallery_probe_metrics(
        predictions,
        gallery,
        np.asarray(["a", "a", "b", "b"]),
        np.asarray(["a", "b"]),
    )
    assert metrics["top1_linkage"] == 1.0
    assert metrics["auroc"] == 1.0


def test_identity_clustered_top1_interval_is_deterministic():
    gallery = np.eye(3, dtype=np.float32)
    predictions = np.asarray(
        [[1, 0, 0], [1, 0, 0], [1, 0, 0], [1, 0, 0], [0, 0, 1], [1, 0, 0]],
        dtype=np.float32,
    )
    probe_ids = np.asarray(["a", "a", "b", "b", "c", "c"])
    gallery_ids = np.asarray(["a", "b", "c"])
    first = identity_clustered_top1_interval(
        predictions,
        gallery,
        probe_ids,
        gallery_ids,
        seed=17,
        n_resamples=500,
    )
    second = identity_clustered_top1_interval(
        predictions,
        gallery,
        probe_ids,
        gallery_ids,
        seed=17,
        n_resamples=500,
    )
    assert first == second
    assert first["estimate"] == 0.5
    assert first["identity_clusters"] == 3
    assert first["lower"] <= first["estimate"] <= first["upper"]


def test_paired_interval_preserves_identity_pairing():
    before = {"a": 0.0, "b": 0.25, "c": 0.5}
    after = {"c": 0.75, "a": 0.25, "b": 0.5}
    result = paired_identity_interval(before, after, seed=3)
    assert result["estimate"] == result["lower"] == result["upper"] == 0.25
    assert result == paired_identity_interval(before, after, seed=3)
    with pytest.raises(ValueError):
        paired_identity_interval(before, {"a": 0.25, "b": 0.5, "d": 0.75}, seed=3)


def test_equivalence_containment_is_strict_and_not_chance_inclusion():
    scores = {"a": 0.5, "b": 0.5, "c": 0.5}
    results = exploratory_equivalence_sensitivity(scores, 0.25, (0.1, 0.25, 0.3))
    assert [row["interval_within_margin"] for row in results] == [False, False, True]
    uncertain = exploratory_equivalence_sensitivity({"a": 0, "b": 1}, 0.5, (0.01,))
    assert uncertain[0]["lower"] < 0 < uncertain[0]["upper"]
    assert not uncertain[0]["interval_within_margin"]
    with pytest.raises(ValueError):
        exploratory_equivalence_sensitivity({"a": np.nan, "b": 0}, 0.25)
