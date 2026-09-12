"""Export per-seed multi-exposure metrics without identity-level or biometric data."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]


def collect_runs(results_root: Path) -> list[dict]:
    rows = []
    for path in sorted(results_root.rglob("metrics.json")):
        result = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(result, dict) or "split_identity_counts" not in result or "conditions" not in result:
            continue
        if all("exposures" not in condition for condition in result["conditions"].values()):
            continue
        config_path = path.parent / "run_config.yaml"
        config = yaml.safe_load(config_path.read_text(encoding="utf-8")) if config_path.exists() else {}
        config_hash = hashlib.sha256(config_path.read_bytes()).hexdigest() if config_path.exists() else "unavailable"
        description = str(result.get("dataset", "")).upper()
        dataset = next((name for name in ("MOBIO", "LFW", "FEI") if name in description), "other")
        common = {
            "source_metrics": "results/" + path.relative_to(results_root).as_posix(),
            "metrics_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "config_sha256": config_hash,
            "embedding_manifest_sha256": hashlib.sha256(json.dumps(result.get("embedding_manifest", {}), sort_keys=True).encode()).hexdigest(),
            "git_commit": result.get("git_commit", "unavailable"),
            "stage": result.get("stage", "exploratory"), "dataset": dataset,
            "scheme": result.get("protection", {}).get("scheme", "biohash"),
            "split_seed": result.get("split_reassignment_seed") or "original",
            "key_seed": config.get("key_seed", "unavailable"), "set_seed": config.get("set_seed", "unavailable"),
            "test_identities": result["split_identity_counts"]["test"],
        }
        for condition, condition_result in result["conditions"].items():
            for exposure, exposure_result in condition_result["exposures"].items():
                for model, model_result in exposure_result["models"].items():
                    for run in model_result["runs"]:
                        interval = run["top1_identity_clustered_interval"]
                        rows.append({**common, "condition": condition, "exposures": int(exposure), "model": model,
                                     "seed": run["seed"], "top1": run["top1_linkage"], "top5": run["top5_linkage"],
                                     "auroc": run["auroc"], "eer": run["eer"], "tar_at_far_1e-2": run["tar_at_far_1e-2"],
                                     "tar_at_far_1e-3": run["tar_at_far_1e-3"], "lower95": interval["lower"],
                                     "upper95": interval["upper"], "best_epoch": run["best_epoch"],
                                     "identity_pairing_available": "identity_top1_scores" in run})
    return rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=ROOT / "results")
    parser.add_argument("--out", type=Path, default=ROOT / "experiments/multiexposure_run_matrix.csv")
    args = parser.parse_args()
    rows = collect_runs(args.results)
    if not rows:
        raise ValueError("No compatible saved multi-exposure runs were found")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{len(rows)} per-seed rows from {len({row['source_metrics'] for row in rows})} local artifacts -> {args.out}")
    print(f"Pilot rows: {sum(row['stage'] == 'pilot' for row in rows)}; unavailable configs: {sum(row['config_sha256'] == 'unavailable' for row in rows)}")
    print(f"Non-multi-exposure artifacts excluded: {len(list(args.results.rglob('metrics.json'))) - len({row['source_metrics'] for row in rows})}")


if __name__ == "__main__":
    main()