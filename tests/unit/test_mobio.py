from pathlib import Path

from biometrics_ai.data.mobio import MobioProtocolConfig, build_mobio_protocol


def test_mobio_protocol_is_session_balanced_and_identity_disjoint(tmp_path: Path):
    for identity in range(12):
        identity_id = f"m{identity:03d}"
        identity_directory = tmp_path / identity_id
        identity_directory.mkdir()
        for session in range(1, 5):
            for question in range(2):
                (identity_directory / f"{identity_id}_{session:02d}_p0{question + 1}_i0_0.jpg").touch()

    config = MobioProtocolConfig(identities=10, samples_per_identity=3, seed=17)
    first = build_mobio_protocol(tmp_path, config)
    second = build_mobio_protocol(tmp_path, config)
    assert first == second
    assert len(first) == 30

    split_ids = {
        split: {str(row["identity_id"]) for row in first if row["split"] == split}
        for split in ("train", "val", "test")
    }
    assert [len(split_ids[split]) for split in ("train", "val", "test")] == [6, 2, 2]
    assert split_ids["train"].isdisjoint(split_ids["val"] | split_ids["test"])
    assert split_ids["val"].isdisjoint(split_ids["test"])
    for identity_id in {str(row["identity_id"]) for row in first}:
        sessions = {str(row["session_id"]) for row in first if row["identity_id"] == identity_id}
        assert len(sessions) == 3