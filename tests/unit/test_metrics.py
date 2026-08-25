import numpy as np
from biometrics_ai.evaluation.metrics import eer, top_k_linkage


def test_metrics():
    assert eer(np.array([1, 1, 0, 0]), np.array([.9, .8, .2, .1])) < .01
    preds = np.eye(3); assert top_k_linkage(preds, preds, np.array([0, 1, 2]), 1) == 1.0
