"""Recover manifest-matching source bytes without modifying the working tree."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import zipfile

ROOT = Path(__file__).resolve().parents[2]


def digest(content: bytes) -> str:
    return hashlib.sha256(content).hexdigest()


def recover_newlines(content: bytes, expected: str) -> tuple[bytes, str] | None:
    if digest(content) == expected:
        return content, "unchanged"
    normalized = content.replace(b"\r\n", b"\n")
    for final_newline in (True, False):
        base = normalized.rstrip(b"\n") + (b"\n" if final_newline else b"")
        for ending, label in ((b"\n", "LF"), (b"\r\n", "CRLF")):
            candidate = base.replace(b"\n", ending)
            if digest(candidate) == expected:
                return candidate, f"{label}; final_newline={final_newline}"
        lines = base.splitlines(keepends=True)
        for boundary in range(1, len(lines)):
            prefix, suffix = b"".join(lines[:boundary]), b"".join(lines[boundary:])
            for candidate, label in (
                (prefix.replace(b"\n", b"\r\n") + suffix, "CRLF/LF"),
                (prefix + suffix.replace(b"\n", b"\r\n"), "LF/CRLF"),
            ):
                if digest(candidate) == expected:
                    return candidate, f"{label}; boundary={boundary}; final_newline={final_newline}"
    return None


def source_candidates(source_root: Path, relative: str, base_commit: str):
    path = source_root / relative
    if path.is_file():
        yield "checkout", path.read_bytes()
    try:
        history = subprocess.run(
            ["git", "log", "--all", "--format=%H", "--", relative],
            cwd=source_root, capture_output=True, text=True,
        )
        if history.returncode != 0:
            return
        for commit in dict.fromkeys([base_commit, *history.stdout.splitlines()]):
            result = subprocess.run(
                ["git", "show", f"{commit}:{relative}"], cwd=source_root, capture_output=True
            )
            if result.returncode == 0:
                yield commit, result.stdout
    except FileNotFoundError:
        return


def recover_manifest(manifest_path: Path, source_root: Path = ROOT) -> tuple[dict[str, bytes], list[dict], list[str]]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    recovered, records, missing = {}, [], []
    for relative, expected in manifest["source_sha256"].items():
        if len(expected) != 64 or any(character not in "0123456789abcdef" for character in expected):
            raise ValueError(f"Invalid SHA-256 for {relative}")
        path = Path(relative)
        if path.is_absolute() or ".." in path.parts or "\\" in relative:
            raise ValueError(f"Unsafe manifest path: {relative}")
        seen = set()
        for source, content in source_candidates(source_root, relative, manifest["base_commit"]):
            if digest(content) in seen:
                continue
            seen.add(digest(content))
            match = recover_newlines(content, expected)
            if match is not None:
                recovered[relative], method = match
                records.append({"path": relative, "sha256": expected, "source": source, "method": method})
                print(f"MATCH {relative}: {source} ({method})", flush=True)
                break
        else:
            missing.append(relative)
            print(f"UNRESOLVED {relative}", flush=True)
    return recovered, records, missing


def write_archive(destination: Path, recovered: dict[str, bytes], manifest_path: Path) -> None:
    expected = json.loads(manifest_path.read_text(encoding="utf-8"))["source_sha256"]
    if set(recovered) != set(expected) or any(digest(recovered[path]) != value for path, value in expected.items()):
        raise ValueError("Refusing to archive incomplete or mismatched recovery")
    with zipfile.ZipFile(destination, "x", compression=zipfile.ZIP_DEFLATED) as archive:
        for relative in sorted(recovered):
            entry = zipfile.ZipInfo(relative, date_time=(2026, 9, 19, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(entry, recovered[relative])
    with zipfile.ZipFile(destination) as archive:
        if any(digest(archive.read(path)) != value for path, value in expected.items()):
            raise ValueError("Archive verification failed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--source-root", type=Path, default=ROOT)
    parser.add_argument("--archive", type=Path)
    args = parser.parse_args()
    recovered, records, missing = recover_manifest(args.manifest, args.source_root)
    if missing:
        raise SystemExit(f"{len(missing)} unresolved files; no archive written")
    if args.archive:
        write_archive(args.archive, recovered, args.manifest)
    print(json.dumps({"sources": records, "verified_sources": len(records), "manifest_sha256": digest(args.manifest.read_bytes()),
                      "archive": str(args.archive) if args.archive else None}, indent=2))


if __name__ == "__main__":
    main()