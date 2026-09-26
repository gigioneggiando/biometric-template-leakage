"""Exploratory precision sensitivity from published marginal variability only."""
from __future__ import annotations

import csv
import hashlib
import json
from math import isfinite, sqrt
from pathlib import Path
from statistics import NormalDist

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "experiments/utility_failure_diagnostics_2026-09-26/variability.csv"
DESTINATION = ROOT / "experiments/utility_precision_planning_2026-09-26"


def precision_scenario(identity_sd: float, key_sd: float, test_people: int,
                       key_draws: int, mean_change: float, variance_multiplier: float = 1.0,
                       tail_alpha: float = .05 / 3, margin: float = .03) -> dict:
    values = (identity_sd, key_sd, mean_change, variance_multiplier, tail_alpha, margin)
    if not all(isfinite(value) for value in values):
        raise ValueError("Planning inputs must be finite")
    if identity_sd < 0 or key_sd < 0 or variance_multiplier <= 0:
        raise ValueError("Invalid variability inputs")
    if any(isinstance(count, bool) or not isinstance(count, int) or count < 2
           for count in (test_people, key_draws)):
        raise ValueError("At least two integer participants and key draws required")
    if not 0 < tail_alpha < .5 or not 0 < margin < 1 or not -1 <= mean_change <= 1:
        raise ValueError("Invalid effect, margin or tail allocation")
    standard_error = sqrt(variance_multiplier * (identity_sd ** 2 / test_people + key_sd ** 2 / key_draws))
    if standard_error == 0:
        raise ValueError("Zero observed variability cannot support this planning approximation")
    critical = NormalDist().inv_cdf(1 - tail_alpha)
    power = NormalDist().cdf((mean_change + margin) / standard_error - critical)
    return {
        "test_people": test_people, "key_draws": key_draws,
        "assumed_mean_tar_change": mean_change, "variance_multiplier": variance_multiplier,
        "tail_alpha": tail_alpha, "margin": margin,
        "proxy_standard_error": standard_error,
        "normal_one_sided_half_width": critical * standard_error,
        "normal_approximation_tar_power": power,
    }


def execute(destination: Path = DESTINATION) -> dict:
    outputs = ("scenarios.csv", "summary.json")
    if any((destination / name).exists() for name in outputs):
        raise FileExistsError("Refusing to overwrite precision planning")
    with SOURCE.open(newline="", encoding="utf-8") as handle:
        variability = list(csv.DictReader(handle))
    if len(variability) != 4:
        raise ValueError("Expected four published historical variability cells")
    rows = []
    for cell in variability:
        for test_people in (40, 100, 200, 400):
            for key_draws in (12, 24, 48, 96):
                for mean_change in (0.0, -.01, -.02):
                    for variance_multiplier in (1.0, 2.0):
                        rows.append({
                            "dataset": cell["dataset"], "split_seed": int(cell["split_seed"]),
                            "historical_people": int(cell["identities"]),
                            "historical_keys": int(cell["key_seeds"]),
                            "identity_axis_sd": float(cell["identity_axis_sd"]),
                            "key_axis_sd": float(cell["seed_axis_sd"]),
                            **precision_scenario(float(cell["identity_axis_sd"]),
                                                 float(cell["seed_axis_sd"]), test_people,
                                                 key_draws, mean_change, variance_multiplier),
                        })
    summary = {
        "status": "completed_exploratory_planning_only", "scenarios": len(rows),
        "new_participants": 0, "new_biometric_evaluations": 0,
        "independent_validation_completed": False, "joint_power_established": False,
        "formula": "SE_proxy^2 = variance_multiplier * (identity_axis_sd^2 / N + key_axis_sd^2 / K)",
        "assumptions": [
            "Treat published marginal axis SDs as variance proxies, not fitted independent components.",
            "Marginal SDs include residual variation; this is not a crossed-ANOVA or hierarchical simulation.",
            "Normal grand-mean approximation with known plug-in variance; variance-estimation uncertainty ignored.",
            "The actual proposed bootstrap gate is not simulated or coverage-calibrated.",
            "Gallery, threshold estimation and new-cohort population shift are not modeled.",
            "Four historical cells overlap; keep separate, do not pool as independent replications.",
            "TAR-only sensitivity at proposed alpha .05/3, not the historical alpha .05/8 or joint power.",
            "No result selects or approves a cohort size, key count, margin or protocol change.",
        ],
        "source_sha256": {
            path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in (Path(__file__), SOURCE)
        },
    }
    destination.mkdir(parents=True, exist_ok=True)
    with (destination / outputs[0]).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    summary["scenarios_sha256"] = hashlib.sha256((destination / outputs[0]).read_bytes()).hexdigest()
    (destination / outputs[1]).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    print(json.dumps(execute(), indent=2))