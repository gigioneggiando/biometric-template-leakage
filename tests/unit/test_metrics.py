import numpy as np
from biometrics_ai.evaluation.metrics import eer, gallery_probe_metrics, top_k_linkage


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
