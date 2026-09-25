import numpy as np
import pytest

from scripts.train.run_scface_utility_confirmation import SEEDS, compare


def records(offset, fmr):
    identities = ["a", "b", "c"]
    return [
        {
            "master_seed": seed,
            "utility": {
                "identities": identities,
                "identity_tar": [0.9 + offset] * 3,
                "identity_fmr": [fmr] * 3,
            },
        }
        for seed in SEEDS
    ]


def test_scface_utility_comparison_uses_frozen_noninferiority_gate():
    passing = compare(records(0, 0.01), records(0.01, 0.01))
    assert passing["utility_pass"]
    assert passing["tar_difference"] == pytest.approx(np.float64(0.01))
    assert not compare(records(0, 0.01), records(-0.04, 0.01))["utility_pass"]
    assert not compare(records(0, 0.01), records(0.01, 0.03))["utility_pass"]
