from pathlib import Path

import numpy as np
import pytest

from biometrics_ai.protection.biohash import BioHashConfig
from biometrics_ai.protection.iomgrp import IoMGRPConfig
from biometrics_ai.protection.polyprotect import PolyProtectConfig
from biometrics_ai.protection.source_analysis_v3 import analyse_source_v3
from biometrics_ai.protection.syntactic_baseline import analyse_syntax
from scripts.diagnostics import protection_policy_recipes as recipes


ROOT = Path(__file__).resolve().parents[2]
SOURCE = (ROOT / "scripts/diagnostics/protection_policy_recipes.py").read_text()
ENTRIES = [
    "biohash_recurring", "biohash_fresh", "iomgrp_recurring", "iomgrp_fresh",
    "polyprotect_recurring", "polyprotect_fresh",
]


@pytest.mark.parametrize("entry", ENTRIES)
def test_v3_traces_real_scheme_recipes_while_syntax_baseline_abstains(entry):
    expected = "reuse" if entry.endswith("recurring") else "conditional_fresh"
    result = analyse_source_v3(SOURCE, entry)
    assert result["decision"] == expected
    assert result["complete"]
    assert len(result["sinks"]) == 1
    assert result["sinks"][0]["trace"][-1] == entry
    assert analyse_syntax(SOURCE, entry)["decision"] == "unknown"


@pytest.mark.parametrize(
    "entry, config, expected_shape",
    [
        ("biohash_fresh", BioHashConfig(512, 64, haar_sign_corrected=True), (64,)),
        ("iomgrp_fresh", IoMGRPConfig(512, 8, 4), (32,)),
        ("polyprotect_fresh", PolyProtectConfig(512, 5, 2, 50), (170,)),
    ],
)
def test_fresh_recipes_execute_the_repository_implementations(entry, config, expected_shape):
    embedding = np.random.default_rng(41).normal(size=512).astype(np.float32)
    assert getattr(recipes, entry)(embedding, 101, 7, config).shape == expected_shape


def test_syntax_baseline_handles_direct_and_local_assignment_syntax():
    direct = "from biometrics_ai.protection.biohash import biohash\ndef f(x, record_id, c):\n    return biohash(x, record_id, c)\n"
    fixed = "from biometrics_ai.protection.biohash import biohash\ndef f(x, record_id, c):\n    return biohash(x, 3, c)\n"
    assigned = "from biometrics_ai.protection.biohash import biohash, generate_key as derive\ndef f(x, master, record_id, c):\n    token = derive(master, 'x', record_id)\n    return biohash(x, token, c)\n"
    assert analyse_syntax(direct, "f")["decision"] == "conditional_fresh"
    assert analyse_syntax(fixed, "f")["decision"] == "reuse"
    assert analyse_syntax(assigned, "f")["decision"] == "conditional_fresh"
