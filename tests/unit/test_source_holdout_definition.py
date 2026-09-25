import ast
import hashlib

from scripts.diagnostics.source_holdout_cases import CASES


def test_holdout_definition_is_balanced_unique_and_parseable():
    assert len(CASES) == 24
    assert {case["label"] for case in CASES} == {"fresh", "reuse"}
    assert {label: sum(case["label"] == label for case in CASES) for label in ("fresh", "reuse")} == {
        "fresh": 12,
        "reuse": 12,
    }
    assert len({case["case"] for case in CASES}) == len(CASES)
    assert len({hashlib.sha256(case["source"].encode()).hexdigest() for case in CASES}) == len(CASES)
    for case in CASES:
        ast.parse(case["source"])
        assert case["rationale"]
