from __future__ import annotations
import argparse, csv
from pathlib import Path


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def load_splits(directory: Path, manifest: Path | None) -> dict[str, list[dict[str, str]]]:
    if manifest is None:
        return {
            name: rows(directory / f"{name}.csv")
            for name in ("train", "val", "test")
            if (directory / f"{name}.csv").exists()
        }
    entries = rows(manifest)
    loaded = {name: [] for name in ("train", "val", "test")}
    for row in entries:
        split = row.get("split")
        if split not in loaded:
            raise SystemExit(f"Unknown or missing split {split!r} in {manifest}")
        loaded[split].append(row)
    return loaded


def main() -> None:
    parser = argparse.ArgumentParser(description="Fail on identity/sample/key collisions across split manifests.")
    parser.add_argument("--splits", type=Path, default=Path("data/processed/splits"))
    parser.add_argument("--manifest", type=Path, help="Single CSV containing a split column")
    args = parser.parse_args()
    loaded = load_splits(args.splits, args.manifest)
    if not loaded:
        raise SystemExit("No split CSVs found")
    critical = []
    for field in ("identity_id", "sample_id", "template_id", "key_id"):
        seen: dict[str, str] = {}
        for split, entries in loaded.items():
            for row in entries:
                value = row.get(field)
                if value and value in seen and seen[value] != split:
                    critical.append(f"{field} collision {value}: {seen[value]} vs {split}")
                elif value and value in seen and field in ("sample_id", "template_id"):
                    critical.append(f"duplicate {field} {value} within {split}")
                elif value:
                    seen[value] = split
    if critical:
        raise SystemExit("CRITICAL LEAKAGE:\n" + "\n".join(critical))
    counts = ", ".join(f"{split}={len(entries)}" for split, entries in loaded.items())
    print(f"Leakage check passed ({counts})")


if __name__ == "__main__":
    main()
