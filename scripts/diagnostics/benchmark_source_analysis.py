"""Same-author source stress cases with separate finite-domain runtime labels."""
from __future__ import annotations

import csv
import hashlib
from importlib.metadata import version
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from biometrics_ai.protection.biohash import generate_key
from biometrics_ai.protection.policy import analyse_policy
from biometrics_ai.protection.source_analysis import analyse_source


def corpus() -> list[dict]:
    header = "from biometrics_ai.protection.biohash import generate_key as derive, biohash as protect, correlated_biohash\n"
    cases = []
    expressions = ["0", "91", "record_id % 4", "record_id & 7", "record_id * 0",
                   "record_id", "record_id + 17", "3 * record_id - 11", "27 - record_id",
                   "derive(master, 'slots', record_id) % 4", "(record_id + 9) & 3",
                   "(record_id * 5 + 11) % 7", "record_id // 4", "record_id - record_id"]
    for index, expression in enumerate(expressions):
        cases.append({"case": f"expression_{index:02d}", "source": header +
                      f"def implementation(embedding, master, record_id, config):\n    allocation = {expression}\n    token = derive(master, 'protection', allocation)\n    return protect(embedding, token, config)\n"})
    for index, expression in enumerate(["sample * 7 + 2", "sample % 5", "derive(secret, 'hidden', sample) & 3"]):
        cases.append({"case": f"helper_{index:02d}", "source": header +
                      f"def helper(secret, sample):\n    renamed = derive\n    return renamed(secret, 'domain', {expression})\ndef implementation(embedding, master, record_id, config):\n    result = helper(master, record_id)\n    return protect(embedding, result, config)\n"})
    for width in [0, 16, 64]:
        cases.append({"case": f"prefix_{width}", "source": header +
                      f"def implementation(embedding, master, record_id, config):\n    common = derive(master, 'common', 0)\n    private = derive(master, 'private', record_id)\n    return correlated_biohash(embedding, common, private, {width}, config)\n"})
    cases.append({"case": "branch_reuse", "source": header +
                  "def implementation(embedding, master, record_id, config):\n    if record_id % 2:\n        return protect(embedding, 3, config)\n    return protect(embedding, 7, config)\n"})
    cases.append({"case": "external_random_pool", "source": "import random\n" + header +
                  "def implementation(embedding, master, record_id, config):\n    generator = random.Random(record_id)\n    token = generator.randrange(4)\n    return protect(embedding, token, config)\n"})
    for shared in [True, False]:
        first_index = "0" if shared else "record_id"
        cases.append({"case": f"assembled_blocks_{shared}", "source": header +
                      "import numpy as np\nfrom biometrics_ai.protection.biohash import _orthonormal_projection as basis\n" +
                      f"def implementation(embedding, master, record_id, config):\n    first = basis(512, 16, derive(master, 'first', {first_index}), True)\n    second = basis(512, 48, derive(master, 'second', record_id), True)\n    assembled = np.concatenate([first, second], axis=1)\n    return embedding @ assembled >= 0\n"})
    return cases


def runtime_label(source: str) -> dict:
    import ast
    import random
    import numpy as np

    class Probe:
        def __matmul__(self, matrix):
            return Projected(matrix)

    class Projected:
        def __init__(self, matrix):
            self.matrix = matrix

        def __ge__(self, threshold):
            return tuple(self.matrix[0])

    tree = ast.parse(source)
    tree.body = [node for node in tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))]
    environment = {"derive": generate_key, "random": random,
                   "np": np, "basis": lambda input_dim, width, key, corrected: np.full((1, width), key, dtype=object),
                   "protect": lambda embedding, key, config: (key,),
                   "correlated_biohash": lambda embedding, shared, private, width, config:
                   (shared, private) if 0 < width < 64 else (shared,) if width == 64 else (private,)}
    exec(compile(tree, "<trusted-generated-corpus>", "exec"), environment)
    try:
        labels = [environment["implementation"](Probe(), 92591, record, None) for record in range(64)]
        repeated = any(len({row[component] for row in labels}) < len(labels) for component in range(len(labels[0])))
        return {"oracle": "reuse_observed" if repeated else "no_reuse_observed",
                "records": len(labels), "component_unique_counts": [len({row[index] for row in labels}) for index in range(len(labels[0]))]}
    except Exception as error:
        return {"oracle": "unlabeled", "error": type(error).__name__}


def evaluate(destination: Path) -> dict:
    if destination.exists():
        raise FileExistsError("Benchmark outputs already exist")
    cases = corpus()
    destination.mkdir(parents=True)
    case_directory = destination / "cases"
    case_directory.mkdir()
    for case in cases:
        path = case_directory / f"{case['case']}.py"
        path.write_text(case["source"], encoding="utf-8")
        case["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
    (destination / "corpus.json").write_text(json.dumps(cases, indent=2) + "\n")
    declared = {"template_dim": 64, "protection": {"scheme": "biohash", "haar_sign_corrected": True},
                "conditions": ["independent_unseen_keys"]}
    config_alert = any(finding["rule"] == "KEY_REUSE" for finding in analyse_policy(declared)["findings"])
    rows, details = [], []
    for case in cases:
        oracle = runtime_label(case["source"])
        started = time.perf_counter()
        result = analyse_source(case["source"], "implementation")
        elapsed = time.perf_counter() - started
        process = subprocess.run([sys.executable, "-m", "bandit", "-q", "-f", "json",
                                  str(case_directory / f"{case['case']}.py")], capture_output=True, text=True)
        if process.returncode not in {0, 1}:
            raise RuntimeError(process.stderr)
        bandit = json.loads(process.stdout)
        if bandit.get("errors"):
            raise RuntimeError("Bandit did not analyze all requested files")
        (destination / f"bandit_{case['case']}.json").write_text(json.dumps(bandit, indent=2) + "\n")
        rows.append({"case": case["case"], "oracle": oracle["oracle"], "source_decision": result["decision"],
                     "source_complete": result["complete"], "configuration_reuse_alert": config_alert,
                     "bandit_any_alert": bool(bandit["results"]),
                     "bandit_rules": ";".join(sorted({finding["test_id"] for finding in bandit["results"]})),
                     "source_seconds": elapsed, "independent_reviewer_label": ""})
        details.append({"case": case["case"], "runtime": oracle, "analysis": result})
    metrics = {}
    for name in ("source", "configuration", "bandit"):
        counts = dict(tp=0, fp=0, tn=0, fn=0, abstain=0, unlabeled=0)
        for row in rows:
            if row["oracle"] == "unlabeled":
                counts["unlabeled"] += 1
                continue
            if name == "source" and row["source_decision"] == "unknown":
                counts["abstain"] += 1
                continue
            predicted = row["source_decision"] == "reuse" if name == "source" else row[f"{name}_reuse_alert"] if name == "configuration" else row["bandit_any_alert"]
            actual = row["oracle"] == "reuse_observed"
            counts["tp" if predicted and actual else "fp" if predicted else "fn" if actual else "tn"] += 1
        metrics[name] = counts
    summary = {"cases": len(rows), "bandit_version": version("bandit"), "metrics": metrics,
               "label_status": "same-author corpus, separate finite-domain runtime oracle; independent review pending",
               "comparison_scope": "Bandit generic warnings are not biometric-reuse findings; YAML baseline trusts declared fresh condition"}
    with (destination / "benchmark.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    (destination / "details.json").write_text(json.dumps(details, indent=2) + "\n")
    (destination / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    return summary


if __name__ == "__main__":
    print(json.dumps(evaluate(ROOT / "experiments/source_security_utility_2026-09-25/benchmark"), indent=2))