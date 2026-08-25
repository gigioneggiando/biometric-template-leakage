from __future__ import annotations
import argparse, csv
from pathlib import Path


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Fail on identity/sample/key collisions across split manifests.")
    parser.add_argument("--splits", type=Path, default=Path("data/processed/splits"))
    args = parser.parse_args()
    loaded = {name: rows(args.splits / f"{name}.csv") for name in ("train", "val", "test") if (args.splits / f"{name}.csv").exists()}
    if not loaded:
        raise SystemExit("No split CSVs found")
    critical = []
    for field in ("identity_id", "sample_id", "template_id"):
        seen: dict[str, str] = {}
        for split, entries in loaded.items():
            for row in entries:
                value = row.get(field)
                if value and value in seen and seen[value] != split:
                    critical.append(f"{field} collision {value}: {seen[value]} vs {split}")
                elif value:
                    seen[value] = split
    if critical:
        raise SystemExit("CRITICAL LEAKAGE:\n" + "\n".join(critical))
    print("Leakage check passed")


if __name__ == "__main__":
    main()
