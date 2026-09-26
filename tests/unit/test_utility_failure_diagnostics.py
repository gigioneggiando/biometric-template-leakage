import json

import pytest

from scripts.diagnostics.analyse_utility_failure import paired_arrays, variability_rows


def write_record(root, dataset, split, seed, policy, identities, tar, threshold):
    payload = {
        "utility": {
            "identities": identities,
            "identity_tar": tar,
            "threshold": threshold,
        }
    }
    (root / f"{dataset}_{split}_{seed}_{policy}.json").write_text(json.dumps(payload))


def test_variability_diagnostics_preserve_pairing(tmp_path, monkeypatch):
    from scripts.train import run_scface_utility_confirmation as study

    monkeypatch.setattr(study, "SEEDS", [1, 2])
    monkeypatch.setattr(study, "SPLITS", [3, 4])
    monkeypatch.setattr(study, "DATASETS", {"MOBIO": "unused"})
    for split in study.SPLITS:
        for seed, shift in [(1, 0.01), (2, 0.02)]:
            write_record(tmp_path, "MOBIO", split, seed, "recurring", ["a", "b"], [0.8, 0.9], 0.5)
            write_record(tmp_path, "MOBIO", split, seed, "separated", ["a", "b"],
                         [0.8 + shift, 0.9 + shift], 0.51)
    _, _, identities, baseline, candidate = paired_arrays(tmp_path, "MOBIO", 3)
    assert identities == ["a", "b"]
    assert (candidate - baseline).mean() == pytest.approx(0.015)
    rows, overlaps = variability_rows(tmp_path)
    assert len(rows) == 2
    assert rows[0]["seed_axis_sd"] > 0
    assert overlaps["MOBIO"] == {"test_identities_per_split": 2, "overlap": 2}
