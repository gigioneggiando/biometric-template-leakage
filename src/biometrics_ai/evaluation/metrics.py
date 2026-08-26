from __future__ import annotations

import numpy as np
from sklearn.metrics import roc_auc_score, roc_curve


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    return np.sum(a * b, axis=-1) / (np.linalg.norm(a, axis=-1) * np.linalg.norm(b, axis=-1) + 1e-12)


def eer(labels: np.ndarray, scores: np.ndarray) -> float:
    fpr, tpr, _ = roc_curve(labels, scores)
    fnr = 1.0 - tpr
    index = np.argmin(np.abs(fpr - fnr))
    return float((fpr[index] + fnr[index]) / 2)


def tar_at_far(labels: np.ndarray, scores: np.ndarray, far: float) -> float:
    fpr, tpr, _ = roc_curve(labels, scores)
    valid = np.where(fpr <= far)[0]
    return float(tpr[valid[-1]]) if len(valid) else 0.0


def top_k_linkage(predictions: np.ndarray, gallery: np.ndarray, identity_ids: np.ndarray, k: int = 1) -> float:
    scores = predictions @ gallery.T
    ranks = np.argsort(-scores, axis=1)[:, :k]
    return float(np.mean([identity_ids[i] in identity_ids[ranks[i]] for i in range(len(identity_ids))]))


def gallery_probe_metrics(
    predictions: np.ndarray,
    gallery: np.ndarray,
    probe_identity_ids: np.ndarray,
    gallery_identity_ids: np.ndarray,
) -> dict[str, float]:
    predictions = np.asarray(predictions, dtype=np.float64)
    gallery = np.asarray(gallery, dtype=np.float64)
    predictions /= np.linalg.norm(predictions, axis=1, keepdims=True).clip(min=1e-12)
    gallery /= np.linalg.norm(gallery, axis=1, keepdims=True).clip(min=1e-12)
    scores = predictions @ gallery.T
    matches = np.asarray(probe_identity_ids)[:, None] == np.asarray(gallery_identity_ids)[None, :]
    if not np.all(matches.sum(axis=1) == 1):
        raise ValueError("Each probe must have exactly one matching gallery identity")
    genuine_scores = scores[matches]
    impostor_scores = scores[~matches]
    ranks = np.argsort(-scores, axis=1)
    ranked_identity_ids = np.asarray(gallery_identity_ids)[ranks]
    probe_identity_ids = np.asarray(probe_identity_ids)
    top5_width = min(5, gallery.shape[0])
    return {
        "mean_genuine_cosine": float(genuine_scores.mean()),
        "mean_impostor_cosine": float(impostor_scores.mean()),
        "top1_linkage": float(np.mean(ranked_identity_ids[:, 0] == probe_identity_ids)),
        "top5_linkage": float(np.mean(np.any(ranked_identity_ids[:, :top5_width] == probe_identity_ids[:, None], axis=1))),
        **verification_metrics(genuine_scores, impostor_scores),
    }


def verification_metrics(genuine_scores: np.ndarray, impostor_scores: np.ndarray) -> dict[str, float]:
    labels = np.concatenate([np.ones(len(genuine_scores)), np.zeros(len(impostor_scores))])
    scores = np.concatenate([genuine_scores, impostor_scores])
    return {"auroc": float(roc_auc_score(labels, scores)), "eer": eer(labels, scores),
            "tar_at_far_1e-2": tar_at_far(labels, scores, 1e-2), "tar_at_far_1e-3": tar_at_far(labels, scores, 1e-3)}
