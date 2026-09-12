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


def identity_clustered_top1_interval(
    predictions: np.ndarray,
    gallery: np.ndarray,
    probe_identity_ids: np.ndarray,
    gallery_identity_ids: np.ndarray,
    *,
    seed: int,
    n_resamples: int = 2000,
    confidence: float = 0.95,
) -> dict[str, float | int]:
    if n_resamples < 1:
        raise ValueError("n_resamples must be positive")
    if not 0.0 < confidence < 1.0:
        raise ValueError("confidence must be between zero and one")

    predictions = np.asarray(predictions, dtype=np.float64)
    gallery = np.asarray(gallery, dtype=np.float64)
    predictions = predictions / np.linalg.norm(predictions, axis=1, keepdims=True).clip(min=1e-12)
    gallery = gallery / np.linalg.norm(gallery, axis=1, keepdims=True).clip(min=1e-12)
    probe_identity_ids = np.asarray(probe_identity_ids)
    gallery_identity_ids = np.asarray(gallery_identity_ids)
    predicted_ids = gallery_identity_ids[np.argmax(predictions @ gallery.T, axis=1)]
    correctness = predicted_ids == probe_identity_ids

    identities = np.unique(probe_identity_ids)
    cluster_successes = np.asarray(
        [correctness[probe_identity_ids == identity].sum() for identity in identities],
        dtype=np.float64,
    )
    cluster_sizes = np.asarray(
        [(probe_identity_ids == identity).sum() for identity in identities],
        dtype=np.float64,
    )
    rng = np.random.default_rng(seed)
    sampled_clusters = rng.integers(0, len(identities), size=(n_resamples, len(identities)))
    estimates = cluster_successes[sampled_clusters].sum(axis=1) / cluster_sizes[sampled_clusters].sum(axis=1)
    alpha = (1.0 - confidence) / 2.0
    return {
        "estimate": float(correctness.mean()),
        "lower": float(np.quantile(estimates, alpha)),
        "upper": float(np.quantile(estimates, 1.0 - alpha)),
        "confidence": confidence,
        "resamples": n_resamples,
        "identity_clusters": len(identities),
        "seed": seed,
    }


def paired_identity_interval(
    reference: dict[str, float], target: dict[str, float], *, seed: int,
    n_resamples: int = 2000, confidence: float = 0.95,
) -> dict[str, float | int]:
    if set(reference) != set(target) or len(reference) < 2:
        raise ValueError("Paired inference requires matching sets of at least two identities")
    if n_resamples < 1 or not 0 < confidence < 1:
        raise ValueError("Invalid bootstrap resamples or confidence")
    identities = sorted(reference)
    before = np.asarray([reference[identity] for identity in identities], dtype=np.float64)
    after = np.asarray([target[identity] for identity in identities], dtype=np.float64)
    if not (np.isfinite(before).all() and np.isfinite(after).all()
            and ((before >= 0) & (before <= 1)).all() and ((after >= 0) & (after <= 1)).all()):
        raise ValueError("Identity-level top-1 rates must be finite values in [0,1]")
    differences = after - before
    sampled = np.random.default_rng(seed).integers(0, len(identities), size=(n_resamples, len(identities)))
    estimates = differences[sampled].mean(axis=1)
    alpha = (1 - confidence) / 2
    return {"estimate": float(differences.mean()), "lower": float(np.quantile(estimates, alpha)),
            "upper": float(np.quantile(estimates, 1 - alpha)), "confidence": confidence,
            "resamples": n_resamples, "identity_clusters": len(identities), "seed": seed}


def exploratory_equivalence_sensitivity(
    scores: dict[str, float], chance: float, margins: tuple[float, ...] = (0.01, 0.02, 0.05),
    *, seed: int = 91223, n_resamples: int = 2000,
) -> list[dict]:
    if not 0 < chance < 1 or any(not np.isfinite(margin) or not 0 < margin < 1 for margin in margins):
        raise ValueError("Chance and sensitivity margins must be in (0,1)")
    interval = paired_identity_interval({identity: chance for identity in scores}, scores,
                                        seed=seed, n_resamples=n_resamples, confidence=0.90)
    return [{**interval, "margin": margin,
             "interval_within_margin": interval["lower"] > -margin and interval["upper"] < margin,
             "analysis": "exploratory 90% interval containment; not confirmatory equivalence"}
            for margin in margins]


def verification_metrics(genuine_scores: np.ndarray, impostor_scores: np.ndarray) -> dict[str, float]:
    labels = np.concatenate([np.ones(len(genuine_scores)), np.zeros(len(impostor_scores))])
    scores = np.concatenate([genuine_scores, impostor_scores])
    return {"auroc": float(roc_auc_score(labels, scores)), "eer": eer(labels, scores),
            "tar_at_far_1e-2": tar_at_far(labels, scores, 1e-2), "tar_at_far_1e-3": tar_at_far(labels, scores, 1e-3)}
