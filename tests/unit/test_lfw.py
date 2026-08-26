from pathlib import Path

from biometrics_ai.data.lfw import LfwProtocolConfig, build_lfw_protocol


def test_lfw_protocol_is_deterministic_and_identity_disjoint(tmp_path: Path):
    for identity in range(12):
        identity_directory = tmp_path / f"person_{identity:02d}"
        identity_directory.mkdir()
        for sample in range(4):
            (identity_directory / f"image_{sample:02d}.jpg").touch()

    config = LfwProtocolConfig(identities=10, samples_per_identity=3, seed=17)
    first = build_lfw_protocol(tmp_path, config)
    second = build_lfw_protocol(tmp_path, config)
    assert first == second
    assert len(first) == 30

    split_ids = {
        split: {str(row["identity_id"]) for row in first if row["split"] == split}
        for split in ("train", "val", "test")
    }
    assert [len(split_ids[split]) for split in ("train", "val", "test")] == [6, 2, 2]
    assert split_ids["train"].isdisjoint(split_ids["val"] | split_ids["test"])
    assert split_ids["val"].isdisjoint(split_ids["test"])