from pathlib import Path

import pytest

from biometrics_ai.data.scface import ScfaceProtocolConfig, build_scface_protocol


def _make_scface(root: Path, subjects: int) -> None:
    frontal = root / "mugshot_frontal_cropped_all"
    surveillance = root / "surveillance_cameras_all"
    frontal.mkdir()
    surveillance.mkdir()
    for subject in range(1, subjects + 1):
        (frontal / f"{subject:03d}_frontal.JPG").touch()
        for camera in range(1, 8):
            for distance in range(1, 4):
                (surveillance / f"{subject:03d}_cam{camera}_{distance}.jpg").touch()


def test_scface_protocol_is_deterministic_complete_and_identity_disjoint(tmp_path: Path):
    _make_scface(tmp_path, 10)
    config = ScfaceProtocolConfig(identities=10, seed=7)
    first = build_scface_protocol(tmp_path, config)
    assert first == build_scface_protocol(tmp_path, config)
    assert len(first) == 220

    split_ids = {split: {row["identity_id"] for row in first if row["split"] == split}
                 for split in ("train", "val", "test")}
    assert [len(split_ids[split]) for split in ("train", "val", "test")] == [6, 2, 2]
    assert split_ids["train"].isdisjoint(split_ids["val"] | split_ids["test"])
    assert split_ids["val"].isdisjoint(split_ids["test"])
    for identity in {row["identity_id"] for row in first}:
        rows = sorted((row for row in first if row["identity_id"] == identity), key=lambda row: row["sample_index"])
        assert [row["sample_index"] for row in rows] == list(range(22))
        assert rows[0]["capture_type"] == "visible_mugshot_gallery"
        assert {(row["camera_id"], row["distance_id"]) for row in rows[1:]} == {
            (camera, distance) for camera in range(1, 8) for distance in range(1, 4)
        }


def test_scface_protocol_rejects_incomplete_identity(tmp_path: Path):
    _make_scface(tmp_path, 6)
    (tmp_path / "surveillance_cameras_all" / "006_cam7_3.jpg").unlink()
    with pytest.raises(ValueError, match="only 5"):
        build_scface_protocol(tmp_path, ScfaceProtocolConfig(identities=6, seed=1))
