"""Structural reuse accounting and validation-selected verification thresholds."""
from __future__ import annotations

import numpy as np


def uniform_reuse_envelope(exposures: int, training_records: int, weights: list[float],
                           capacities: list[int | None]) -> dict[str, float]:
    if type(exposures) is not int or exposures < 1 or type(training_records) is not int or training_records < 0:
        raise ValueError("Record counts must be nonnegative integers with at least one exposure")
    if len(weights) != len(capacities) or not weights or not np.isclose(sum(weights), 1):
        raise ValueError("Component weights must sum to one and align with capacities")
    if any(not np.isfinite(weight) or weight <= 0 for weight in weights):
        raise ValueError("Weights must be positive and finite")
    if any(capacity is not None and (type(capacity) is not int or capacity < 1) for capacity in capacities):
        raise ValueError("Capacities must be positive integers or None for ideal fresh keys")
    edges = exposures * training_records + exposures * (exposures - 1) // 2
    probabilities = [0.0 if capacity is None else 1 / capacity for capacity in capacities]
    return {"comparison_edges": edges,
            "expected_reused_component_mass": float(edges * np.dot(weights, probabilities)),
            "ideal_bad_event_upper": float(min(1, edges * sum(probabilities)))}


def validation_threshold(impostor_scores: np.ndarray, target_fmr: float) -> float:
    values = np.asarray(impostor_scores, dtype=float).ravel()
    if values.size == 0 or not np.isfinite(values).all() or not 0 < target_fmr < 1:
        raise ValueError("Finite nonempty validation scores and a target FMR in (0, 1) required")
    candidates = np.unique(values)
    permitted = int(np.floor(target_fmr * len(values)))
    boundary = np.sort(values)[len(values) - permitted - 1]
    threshold = float(np.nextafter(boundary, np.inf))
    assert (values >= threshold).sum() <= permitted
    return threshold


def paired_mean_interval(differences: np.ndarray, seed: int, resamples: int = 2000,
                         alpha: float = .05) -> tuple[float, float]:
    values = np.asarray(differences, dtype=float)
    if values.ndim != 2 or min(values.shape) < 2 or not np.isfinite(values).all():
        raise ValueError("Expected finite key/model-seed by identity differences")
    if resamples < 1 or not 0 < alpha < .5:
        raise ValueError("Invalid interval settings")
    random = np.random.default_rng(seed)
    seeds = random.integers(values.shape[0], size=(resamples, values.shape[0]))
    identities = random.integers(values.shape[1], size=(resamples, values.shape[1]))
    estimates = values[seeds[:, :, None], identities[:, None, :]].mean(axis=(1, 2))
    return tuple(float(value) for value in np.quantile(estimates, [alpha, 1 - alpha]))


def acceptance_gate(leakage_lower: float, utility_lower: float, candidate_fmr_upper: float,
                    utility_margin: float, fmr_limit: float) -> bool:
    values = [leakage_lower, utility_lower, candidate_fmr_upper, utility_margin, fmr_limit]
    if not np.isfinite(values).all() or not 0 <= utility_margin < 1 or not 0 < fmr_limit < 1:
        raise ValueError("Invalid acceptance criteria")
    return bool(leakage_lower > 0 and utility_lower >= -utility_margin and candidate_fmr_upper <= fmr_limit)