"""Verify frozen source bytes with explicit checkout conversions or snapshots."""
from __future__ import annotations

from collections.abc import Collection
import hashlib
from pathlib import Path
import zipfile


def verify_source(
    path: Path, expected_hashes: Collection[str], snapshot: tuple[Path, str] | None = None,
) -> dict[str, str]:
    if not expected_hashes:
        raise ValueError("An existing manifest hash is required")
    if snapshot is not None:
        archive_path, member = snapshot
        with zipfile.ZipFile(archive_path) as archive:
            raw = archive.read(member)
        candidates = [("snapshot_exact", raw)]
    else:
        raw = path.read_bytes()
        lf = raw.replace(b"\r\n", b"\n")
        candidates = [("checkout_exact", raw), ("checkout_to_lf", lf),
                      ("checkout_to_crlf", lf.replace(b"\n", b"\r\n"))]
    for mode, content in candidates:
        digest = hashlib.sha256(content).hexdigest()
        if digest in expected_hashes:
            return {"sha256": digest, "mode": mode}
    raise ValueError(f"Source does not match frozen manifest: {path}")