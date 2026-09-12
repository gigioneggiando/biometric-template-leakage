from pathlib import Path

import pytest

from biometrics_ai.data.fei import FeiProtocolConfig, build_fei_protocol


def _make_fei(root: Path, subjects: int, poses: int) -> None:
    for subject in range(1, subjects + 1):
        for pose in range(1, poses + 1):
            (root / f"{subject}-{pose:02d}.jpg").touch()


def test_fei_protocol_is_deterministic_identity_disjoint_and_keeps_pose(tmp_path: Path):
    _make_fei(tmp_path, subjects=10, poses=14)
    config = FeiProtocolConfig(identities=10, samples_per_identity=12, seed=3)

    first = build_fei_protocol(tmp_path, config)
    assert first == build_fei_protocol(tmp_path, config)
    assert len(first) == 120

    split_ids = {s: {r["identity_id"] for r in first if r["split"] == s} for s in ("train", "val", "test")}
    assert [len(split_ids[s]) for s in ("train", "val", "test")] == [6, 2, 2]
    assert split_ids["train"].isdisjoint(split_ids["val"] | split_ids["test"])
    assert split_ids["val"].isdisjoint(split_ids["test"])
    assert all(1 <= int(r["pose_id"]) <= 14 for r in first)
    per_identity = {r["identity_id"] for r in first}
    for identity in per_identity:
        indices = sorted(int(r["sample_index"]) for r in first if r["identity_id"] == identity)
        assert indices == list(range(12))


def test_fei_protocol_rejects_identities_with_too_few_images(tmp_path: Path):
    _make_fei(tmp_path, subjects=6, poses=8)
    with pytest.raises(ValueError):
        build_fei_protocol(tmp_path, FeiProtocolConfig(identities=6, samples_per_identity=12, seed=1))
