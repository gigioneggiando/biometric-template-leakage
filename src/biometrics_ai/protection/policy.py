"""Static key-scope analysis of the repository's experiment configuration DSL."""
from __future__ import annotations

import argparse
import copy
from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re

import yaml


SUPPORTED_SCHEMES = {
    "biohash", "mlphash_paper_specified", "iomgrp_paper_specified", "polyprotect_paper_specified",
}


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    path: str
    message: str


def analyse_policy(config: dict) -> dict:
    """Interpret declared key scope without reading templates or fitting an attacker."""
    findings: list[Finding] = []
    scopes = []

    def add(rule: str, severity: str, path: str, message: str) -> None:
        findings.append(Finding(rule, severity, path, message))

    if not isinstance(config, dict):
        return {"decision": "block", "scopes": [], "findings": [asdict(Finding(
            "INVALID_CONFIG", "error", "$", "Expected a configuration mapping."))]}
    schemes = config.get("schemes", [{"protection": config.get("protection", {"scheme": "biohash"}),
                                       "template_dim": config.get("template_dim")}])
    conditions = config.get("conditions")
    if not isinstance(schemes, list) or not schemes or not all(isinstance(item, dict) for item in schemes):
        add("INVALID_CONFIG", "error", "schemes", "Expected a nonempty list of scheme mappings.")
        schemes = []
    if not isinstance(conditions, list) or not conditions or not all(isinstance(item, str) for item in conditions):
        add("INVALID_CONFIG", "error", "conditions", "Explicit nonempty conditions are required.")
        conditions = []
    for scheme_index, scheme in enumerate(schemes):
        protection = scheme.get("protection", {})
        path = f"schemes[{scheme_index}]" if "schemes" in config else "protection"
        if not isinstance(protection, dict) or protection.get("scheme") not in SUPPORTED_SCHEMES:
            add("UNKNOWN_SCHEME", "error", path, "Unsupported protection; no security inference is available.")
            continue
        name = protection["scheme"]
        dimension = scheme.get("template_dim")
        if type(dimension) is not int or dimension < 1:
            add("INVALID_CONFIG", "error", path, "A positive integer template_dim is required.")
            continue
        if name == "polyprotect_paper_specified":
            add("NATIVE_LINKAGE_REVIEW", "review", path,
                "PolyProtect is outside the rotational-invariance argument; fresh keys do not establish unlinkability.")
        if name == "biohash" and protection.get("haar_sign_corrected") is not True:
            add("HAAR_ASSUMPTION", "review", path,
                "The ideal Haar argument cannot be inferred from an uncorrected QR configuration.")
        if protection.get("include_key_slot", False):
            add("SLOT_DISCLOSURE", "error", path + ".include_key_slot",
                "Key-slot labels expose transform-group side information; disable for a hidden-slot policy.")
        for condition_index, condition in enumerate(conditions):
            condition_path = f"conditions[{condition_index}]"
            scope = "unknown"
            pool_match = re.fullmatch(r"(?:system|random)_key_pool_([0-9]+)", condition)
            correlation = re.fullmatch(r"correlated_(key|dims)_([0-9]+)", condition)
            if condition == "independent_unseen_keys":
                scope = "fresh_declared"
            elif condition == "shared_key_calibration" or (pool_match and int(pool_match[1]) > 0):
                scope = "shared_across_splits"
                add("KEY_REUSE", "error", condition_path,
                    f"{name}: {condition} permits the same hidden transforms across identities and splits.")
            elif correlation and name == "biohash":
                amount = int(correlation[2])
                valid = (amount in {0, 25, 50, 75, 100} if correlation[1] == "key" else amount <= dimension)
                shared_dimensions = dimension * amount // 100 if correlation[1] == "key" else amount
                if valid:
                    scope = "shared_projection" if shared_dimensions else "fresh_declared"
                    if shared_dimensions:
                        add("KEY_CORRELATION", "error", condition_path,
                            f"{shared_dimensions}/{dimension} projection dimensions are shared across records.")
            if scope == "unknown":
                add("UNKNOWN_CONDITION", "error", condition_path,
                    f"{name}: unsupported or invalid condition {condition!r}; analysis fails closed.")
            scopes.append({"scheme": name, "condition": condition, "scope": scope})
    add("RUNTIME_ASSUMPTIONS", "review", "$",
        "Configuration cannot verify input norms, key secrecy/entropy, unique record IDs, implementation fidelity, "
        "side channels, or authentication utility. Reproducible experiment seeds are not production secrets.")
    return {"algorithm": "key-scope-static-analysis-v1", "decision": "block" if any(
        finding.severity == "error" for finding in findings) else "review",
        "scopes": scopes, "findings": [asdict(finding) for finding in findings]}


def recommend_fresh_policy(config: dict) -> dict:
    """Return a separate research comparison config; never overwrite the supplied policy."""
    audit = analyse_policy(config)
    if any(finding["rule"] in {"INVALID_CONFIG", "UNKNOWN_SCHEME", "UNKNOWN_CONDITION"}
           for finding in audit["findings"]):
        raise ValueError("Unsupported configuration cannot be automatically remediated")
    candidate = copy.deepcopy(config)
    candidate["conditions"] = ["independent_unseen_keys"]
    protections = ([item["protection"] for item in candidate["schemes"]] if "schemes" in candidate
                   else [candidate.setdefault("protection", {"scheme": "biohash"})])
    for protection in protections:
        protection.pop("include_key_slot", None)
    return candidate


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--enforce", action="store_true", help="Exit nonzero until all findings have been reviewed")
    args = parser.parse_args()
    result = analyse_policy(yaml.safe_load(args.config.read_text(encoding="utf-8")))
    print(json.dumps(result, indent=2))
    if args.enforce:
        raise SystemExit(2 if result["decision"] == "block" else 3)


if __name__ == "__main__":
    main()