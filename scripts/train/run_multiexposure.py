from __future__ import annotations
import argparse, csv, json, subprocess, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import numpy as np
import torch
import yaml
from torch.nn import functional as F

from biometrics_ai.aggregation.models import DeepSetsExtractor, SingleTemplateMLP
from biometrics_ai.data.synthetic import SyntheticConfig, build_sets
from biometrics_ai.evaluation.metrics import cosine_similarity, top_k_linkage, verification_metrics
from biometrics_ai.utils.seeding import seed_record_dict


def parse() -> dict:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--exposures", type=int)
    parser.add_argument("--seed", type=int)
    args = parser.parse_args()
    config = yaml.safe_load(args.config.read_text(encoding="utf-8"))
    if args.exposures: config["exposures"] = args.exposures
    if args.seed is not None: config["seed"] = args.seed
    return config


def train(config: dict) -> dict:
    started = time.time()
    seed_record = seed_record_dict(int(config["seed"]))
    synth = SyntheticConfig(**config.get("synthetic", {}), seed=int(config["seed"]))
    exposures = int(config["exposures"])
    train_set = build_sets(synth, "train", exposures, "train")
    val_set = build_sets(synth, "val", exposures, "val")
    test_set = build_sets(synth, "test", exposures, "test")
    input_dim, output_dim = train_set["templates"].shape[-1], train_set["targets"].shape[-1]
    model = SingleTemplateMLP(input_dim, output_dim) if exposures == 1 else DeepSetsExtractor(input_dim, output_dim)
    optimizer = torch.optim.Adam(model.parameters(), lr=float(config.get("learning_rate", 1e-3)))
    x, y = torch.tensor(train_set["templates"]), torch.tensor(train_set["targets"])
    for _ in range(int(config.get("epochs", 80))):
        optimizer.zero_grad()
        prediction = model(x)
        loss = (1 - F.cosine_similarity(prediction, y, dim=-1)).mean() + 0.1 * F.mse_loss(prediction, y)
        loss.backward(); optimizer.step()
    model.eval()
    with torch.no_grad():
        predictions = model(torch.tensor(test_set["templates"])).numpy()
    targets = test_set["targets"]
    genuine = cosine_similarity(predictions, targets)
    impostor = np.asarray([cosine_similarity(predictions[i], targets[(i + 1) % len(targets)]) for i in range(len(targets))])
    metrics = {"mean_cosine": float(genuine.mean()), "normalized_l2": float(np.linalg.norm(predictions-targets, axis=1).mean()),
               "top1_linkage": top_k_linkage(predictions, targets, test_set["identity_ids"], 1), "top5_linkage": top_k_linkage(predictions, targets, test_set["identity_ids"], min(5, len(targets))),
               **verification_metrics(genuine, impostor), "training_loss": float(loss.item()), "elapsed_seconds": time.time()-started}
    run_dir = Path(config.get("results_root", "results/proposed")) / "biohash" / ("single_mlp" if exposures == 1 else "deepsets") / f"exposures_{exposures}" / f"seed_{int(config['seed']):04d}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "run_config.yaml").write_text(yaml.safe_dump(config, sort_keys=True), encoding="utf-8")
    (run_dir / "seeds.json").write_text(json.dumps(seed_record, indent=2), encoding="utf-8")
    (run_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    np.savetxt(run_dir / "predictions.csv", predictions, delimiter=",")
    (run_dir / "git_commit.txt").write_text(subprocess.run(["git", "rev-parse", "HEAD"], text=True, capture_output=True).stdout.strip() or "uncommitted", encoding="utf-8")
    (run_dir / "timing.json").write_text(json.dumps({"elapsed_seconds": metrics["elapsed_seconds"]}, indent=2), encoding="utf-8")
    print(json.dumps({"run_dir": str(run_dir), **metrics}, indent=2))
    return metrics


if __name__ == "__main__":
    train(parse())
