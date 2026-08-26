"""Run a BioHash dimension sweep for Month 1 single-template experiments."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import yaml


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-config", type=Path, required=True)
    parser.add_argument("--template-dims", type=int, nargs="+", default=[64, 128, 256])
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()

    base_config = yaml.safe_load(args.base_config.read_text(encoding="utf-8"))
    runner = Path(__file__).with_name("run_lfw_month1.py")
    summaries = []
    for template_dim in args.template_dims:
        config = dict(base_config)
        config["template_dim"] = template_dim
        results_directory = args.output_root / f"dim_{template_dim:03d}"
        config["results_dir"] = results_directory.as_posix()
        results_directory.mkdir(parents=True, exist_ok=True)
        config_path = results_directory / "input_config.yaml"
        config_path.write_text(yaml.safe_dump(config, sort_keys=True), encoding="utf-8")
        subprocess.run(
            [sys.executable, str(runner), "--config", str(config_path)],
            check=True,
            stdout=subprocess.DEVNULL,
        )
        metrics = json.loads((results_directory / "metrics.json").read_text(encoding="utf-8"))
        independent = metrics["conditions"]["independent_unseen_keys"]["attacker_summary"]
        summaries.append(
            {
                "template_dim": template_dim,
                "top1_mean": independent["top1_linkage"]["mean"],
                "top1_std": independent["top1_linkage"]["std"],
                "auroc_mean": independent["auroc"]["mean"],
                "eer_mean": independent["eer"]["mean"],
            }
        )
    print(json.dumps({"base_config": args.base_config.as_posix(), "runs": summaries}, indent=2))


if __name__ == "__main__":
    main()