from pathlib import Path
import json
import runpy
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[2]
RECOVERY = runpy.run_path(str(ROOT / "scripts/diagnostics/recover_executed_sources.py"))


@pytest.mark.parametrize("expected", [b"one\ntwo\nthree\n", b"one\r\ntwo\r\nthree",
                                     b"one\r\ntwo\nthree\n", b"one\ntwo\r\nthree\r\n"])
def test_recovery_requires_exact_digest(expected):
    match = RECOVERY["recover_newlines"](b"one\ntwo\nthree\n", RECOVERY["digest"](expected))
    assert match is not None
    assert match[0] == expected


def test_recovery_does_not_change_source_text():
    assert RECOVERY["recover_newlines"](b"original\n", RECOVERY["digest"](b"different\n")) is None


def test_recover_from_external_backup_without_git(tmp_path):
    content = b"original\r\nsource\n"
    (tmp_path / "source.py").write_bytes(content)
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"base_commit": "unused", "source_sha256": {
        "source.py": RECOVERY["digest"](content),
    }}))
    recovered, records, missing = RECOVERY["recover_manifest"](manifest, tmp_path)
    assert recovered == {"source.py": content}
    assert records[0]["method"] == "unchanged"
    assert missing == []


@pytest.mark.parametrize("relative, expected", [("../escape.py", "0" * 64), ("source.py", "invalid")])
def test_invalid_manifest_is_rejected(tmp_path, relative, expected):
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"source_sha256": {relative: expected}}))
    with pytest.raises(ValueError):
        RECOVERY["recover_manifest"](manifest, tmp_path)


def test_archive_refuses_partial_recovery_and_preserves_bytes(tmp_path):
    content = b"one\r\ntwo\n"
    manifest = tmp_path / "manifest.json"
    manifest.write_text(json.dumps({"source_sha256": {"source.py": RECOVERY["digest"](content)}}))
    destination = tmp_path / "sources.zip"
    with pytest.raises(ValueError, match="incomplete"):
        RECOVERY["write_archive"](destination, {}, manifest)
    assert not destination.exists()
    RECOVERY["write_archive"](destination, {"source.py": content}, manifest)
    with zipfile.ZipFile(destination) as archive:
        assert archive.read("source.py") == content
    with pytest.raises(FileExistsError):
        RECOVERY["write_archive"](destination, {"source.py": content}, manifest)