import ast
import hashlib

from scripts.diagnostics.source_holdout_v2_confirmation_cases import CASES


def test_v2_confirmation_is_balanced_unique_and_parseable():
    assert len(CASES) == 20
    assert {label: sum(case["label"] == label for case in CASES) for label in ("fresh", "reuse")} == {
        "fresh": 10,
        "reuse": 10,
    }
    assert len({case["case"] for case in CASES}) == len(CASES)
    assert len({hashlib.sha256(case["source"].encode()).hexdigest() for case in CASES}) == len(CASES)
    for case in CASES:
        ast.parse(case["source"])
        assert case["rationale"]
