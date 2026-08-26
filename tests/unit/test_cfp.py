from pathlib import Path

from biometrics_ai.data.cfp import CfpProtocolConfig, build_cfp_protocol


def test_cfp_protocol_is_deterministic_identity_disjoint_and_view_scoped(tmp_path: Path):
    for identity in range(12):
        identity_directory = tmp_path / f"{identity:03d}"
        for view, count in (("frontal", 4), ("profile", 2)):
            view_directory = identity_directory / view
            view_directory.mkdir(parents=True)
            for sample in range(count):
                (view_directory / f"{sample:02d}.jpg").touch()

    config = CfpProtocolConfig(identities=10, samples_per_identity=3, seed=17, views=("frontal",))
    first = build_cfp_protocol(tmp_path, config)
    assert first == build_cfp_protocol(tmp_path, config)
    assert len(first) == 30
    assert {str(row["view"]) for row in first} == {"frontal"}

    split_ids = {
        split: {str(row["identity_id"]) for row in first if row["split"] == split}
        for split in ("train", "val", "test")
    }
    assert [len(split_ids[split]) for split in ("train", "val", "test")] == [6, 2, 2]
    assert split_ids["train"].isdisjoint(split_ids["val"] | split_ids["test"])
    assert split_ids["val"].isdisjoint(split_ids["test"])