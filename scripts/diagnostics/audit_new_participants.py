"""Audit local cohort overlap without treating new splits as new participants."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from biometrics_ai.protection.source_analysis import analyse_source

DESTINATION = ROOT / "experiments/new_participant_joint_2026-09-25"
PRIOR = ROOT / "experiments/source_security_utility_2026-09-25/execution_manifest.json"


def participant_overlap(candidate: list[dict], prior: list[dict], minimum_records: int = 11) -> dict:
    if minimum_records < 2:
        raise ValueError("At least one gallery and one probe record are required")
    for row in candidate + prior:
        if not isinstance(row.get("identity_id"), str) or not row["identity_id"].strip():
            raise ValueError("Nonempty stable identity IDs are required")
    counts = Counter(row["identity_id"] for row in candidate)
    seen = {row["identity_id"] for row in prior}
    eligible = {identity for identity, count in counts.items() if count >= minimum_records}
    return {"records": len(candidate), "participants": len(counts),
            "eligible_participants": len(eligible), "minimum_records": minimum_records,
            "previously_seen_participants": len(set(counts) & seen),
            "eligible_not_seen_by_id": len(eligible - seen),
            "new_participants_verified": 0,
            "identity_check_scope": "Within-source stable IDs only; different IDs do not prove different people",
            "status": "blocked_no_new_ids" if not eligible - seen else "blocked_requires_independent_identity_and_access_review"}


def audit_local(destination: Path = DESTINATION) -> dict:
    prior_manifest = json.loads(PRIOR.read_text(encoding="utf-8"))
    cells = []
    for dataset, directory in [("FEI", "fei_multiexposure"), ("MOBIO", "mobio")]:
        path = ROOT / "data/processed/embeddings" / directory / "buffalo_l_yunet/metadata.json"
        relative = path.relative_to(ROOT).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if prior_manifest["input_sha256"].get(relative) != digest:
            raise ValueError("Prior metadata no longer matches frozen bytes; obtain its archived version")
        records = json.loads(path.read_text(encoding="utf-8"))
        cells.append({"dataset": dataset, "metadata_path": relative, "metadata_sha256": digest,
                      "matches_prior_input_exactly": True, **participant_overlap(records, records)})
    source_path = ROOT / "scripts/diagnostics/source_policy_recipes.py"
    source = source_path.read_text(encoding="utf-8")
    analyses = {name: analyse_source(source, name) for name in ["recurring", "partial", "separated"]}
    result = {"created_utc": datetime.now(timezone.utc).isoformat(),
              "status": "blocked_pending_new_authorized_participants", "new_experiment_run": False,
              "scope": "Existing FEI/MOBIO embedding inputs, not a global search for people",
              "prior_manifest_sha256": hashlib.sha256(PRIOR.read_bytes()).hexdigest(),
              "audit_source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "recipe_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
              "analyzer_sha256": hashlib.sha256((ROOT / "src/biometrics_ai/protection/source_analysis.py").read_bytes()).hexdigest(),
              "cohorts": cells, "source_analysis": analyses,
              "other_local_data": "LFW exists but is not certified new or interchangeable with FEI; cross-source participant review required"}
    destination.mkdir(parents=True, exist_ok=True)
    output = destination / "cohort_audit.json"
    if output.exists():
        raise FileExistsError("Refusing to replace the dated cohort audit")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = audit_local()
    print(json.dumps({"status": result["status"], "cohorts": result["cohorts"],
                      "source_decisions": {key: value["decision"] for key, value in result["source_analysis"].items()}}, indent=2))