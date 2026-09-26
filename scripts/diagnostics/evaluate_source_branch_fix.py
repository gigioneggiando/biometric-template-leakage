"""Record post-fix regression results separately from frozen internal studies."""
from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from biometrics_ai.protection.source_analysis_v2 import analyse_source_v2
from biometrics_ai.protection.source_analysis_v3 import analyse_source_v3
from scripts.diagnostics.source_holdout_cases import CASES as DEVELOPMENT
from scripts.diagnostics.source_holdout_v2_confirmation_cases import CASES as CONFIRMATION
from scripts.diagnostics.evaluate_real_source_integration import ENTRIES, RECIPE_PATH

DESTINATION = ROOT / "experiments/source_branch_fix_2026-09-26"


def evaluate(destination: Path = DESTINATION) -> dict:
    output = destination / "regression.json"
    if output.exists():
        raise FileExistsError("Refusing to replace post-fix regression evidence")
    recipe_source = RECIPE_PATH.read_text(encoding="utf-8")
    integrations = [{"case": name, "source": recipe_source, "entry": name} for name in ENTRIES]
    studies = [
        ("source_holdout_v2_2026-09-25", DEVELOPMENT, analyse_source_v2, "prediction"),
        ("source_holdout_v2_confirmation_2026-09-25", CONFIRMATION, analyse_source_v2, "prediction"),
        ("source_real_integration_2026-09-25", integrations + CONFIRMATION, analyse_source_v3, "v3_prediction"),
    ]
    rows, inputs = [], []
    for study, cases, analyze, prediction_column in studies:
        path = ROOT / "experiments" / study / "results.csv"
        inputs.append(path)
        with path.open(encoding="utf-8", newline="") as handle:
            frozen = {row["case"]: row for row in csv.DictReader(handle)}
        for case in cases:
            previous = frozen[case["case"]]
            if previous.get("outcome") == "excluded_invalid":
                continue
            result = analyze(case["source"], case.get("entry", "implementation"))
            prediction = {"conditional_fresh": "fresh", "reuse": "reuse", "unknown": "abstain"}[result["decision"]]
            rows.append({"study": study, "case": case["case"], "label": previous["label"],
                         "frozen_prediction": previous[prediction_column], "current_prediction": prediction,
                         "changed_prediction": previous[prediction_column] != prediction,
                         "current_complete": result["complete"], "analysis": result})
    source = """from biometrics_ai.protection.biohash import generate_key, biohash
def implementation(embedding, master, record_id, config):
    if record_id % 2:
        return biohash(embedding, generate_key(master, 'same', record_id), config)
    else:
        return biohash(embedding, generate_key(master, 'same', record_id + 1), config)
"""
    namespace = {}
    exec(source, namespace)
    namespace["biohash"] = lambda embedding, key, config: key
    keys = [namespace["implementation"](None, 92591, record, None) for record in range(8)]
    counterexample = {"source": source, "records": len(keys), "distinct_keys": len(set(keys)),
                      "v2": analyse_source_v2(source, "implementation"),
                      "v3": analyse_source_v3(source, "implementation")}
    if len(set(keys)) != 4 or any(counterexample[name]["decision"] != "unknown" for name in ("v2", "v3")):
        raise AssertionError("Cross-path collision regression failed")
    paths = inputs + [Path(__file__), RECIPE_PATH,
                      ROOT / "src/biometrics_ai/protection/source_analysis.py",
                      ROOT / "src/biometrics_ai/protection/source_analysis_v2.py",
                      ROOT / "src/biometrics_ai/protection/source_analysis_v3.py",
                      ROOT / "scripts/diagnostics/source_holdout_cases.py",
                      ROOT / "scripts/diagnostics/source_holdout_v2_confirmation_cases.py"]
    result = {"status": "completed", "created_utc": datetime.now(timezone.utc).isoformat(),
              "scope": "Post-fix internal regression, not independent validation or new biometric evidence",
              "case_evaluations": len(rows), "changed_predictions": sum(row["changed_prediction"] for row in rows),
              "false_fresh": sum(row["current_prediction"] == "fresh" and row["label"] == "reuse" for row in rows),
              "source_and_input_sha256": {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                                          for path in paths},
              "counterexample": counterexample, "cases": rows}
    destination.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = evaluate()
    print(json.dumps({name: result[name] for name in ["status", "case_evaluations", "changed_predictions", "false_fresh"]}, indent=2))