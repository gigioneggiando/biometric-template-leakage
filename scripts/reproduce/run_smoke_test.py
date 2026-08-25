from __future__ import annotations
import json, subprocess, sys
from pathlib import Path


def main() -> None:
    Path("results/reproduced").mkdir(parents=True, exist_ok=True)
    results = []
    for exposures in (1, 2, 5, 10):
        command = [sys.executable, "scripts/train/run_multiexposure.py", "--config", "configs/attacks/proposed_synthetic.yaml", "--exposures", str(exposures), "--seed", "7"]
        completed = subprocess.run(command, text=True, capture_output=True, check=True)
        results.append(json.loads(completed.stdout))
    Path("results/reproduced/smoke_test.json").write_text(json.dumps({"classification": "ENGINEERING VALIDATION, NOT PAPER REPRODUCTION", "runs": results}, indent=2), encoding="utf-8")
    print("Smoke test completed")


if __name__ == "__main__":
    main()
