from pathlib import Path

from biometrics_ai.data.olivetti import OlivettiProtocolConfig, build_olivetti_protocol


def test_olivetti_protocol_is_deterministic_and_identity_disjoint(tmp_path: Path):
    for identity in range(12):
        identity_directory = tmp_path / f"{identity:02d}"
        identity_directory.mkdir()
        for sample in range(4):
            (identity_directory / f"{sample:02d}.png").touch()

    config = OlivettiProtocolConfig(identities=10, samples_per_identity=3, seed=17)
    first = build_olivetti_protocol(tmp_path, config)
    assert first == build_olivetti_protocol(tmp_path, config)
    assert len(first) == 30

    split_ids = {
        split: {str(row["identity_id"]) for row in first if row["split"] == split}
        for split in ("train", "val", "test")
    }
    assert [len(split_ids[split]) for split in ("train", "val", "test")] == [6, 2, 2]
    assert split_ids["train"].isdisjoint(split_ids["val"] | split_ids["test"])
    assert split_ids["val"].isdisjoint(split_ids["test"])