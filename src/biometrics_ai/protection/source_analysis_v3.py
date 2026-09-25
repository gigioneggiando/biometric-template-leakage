"""Scheme-contract extension of source-analysis v2 for repository protections."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path

from .source_analysis import FIXED, UNKNOWN, Provenance
from .source_analysis_v2 import SourceAnalysisV2, Value


MODULES = {
    "biometrics_ai.protection": "biohash",
    "biometrics_ai.protection.biohash": "biohash",
    "biometrics_ai.protection.iomgrp": "iomgrp",
    "biometrics_ai.protection.polyprotect": "polyprotect",
}


class SourceAnalysisV3(SourceAnalysisV2):
    """V2 inference plus explicit IoM-GRP and PolyProtect sink contracts."""

    def __init__(self, source: str):
        self.tree = ast.parse(source)
        self.functions = {}
        self.globals: dict[str, Provenance] = {}
        self.findings: list[dict] = []
        self.sinks: list[dict] = []
        self.active: list[str] = []
        for node in self.tree.body:
            if isinstance(node, ast.FunctionDef):
                self.functions[node.name] = node
                self.globals[node.name] = Provenance(reference=f"local.{node.name}")
            elif isinstance(node, ast.ImportFrom):
                prefix = MODULES.get(node.module or "")
                for alias in node.names:
                    self.globals[alias.asname or alias.name] = (
                        Provenance(reference=f"{prefix}.{alias.name}") if prefix else UNKNOWN
                    )
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    prefix = MODULES.get(alias.name)
                    if prefix and alias.asname:
                        self.globals[alias.asname] = Provenance(reference=prefix)
                    elif alias.name == "numpy":
                        self.globals[alias.asname or "numpy"] = Provenance(reference="numpy")
                    else:
                        self.globals[alias.asname or alias.name.split(".")[0]] = UNKNOWN
            elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        value = self.expression(node.value, {})
                        self.globals[target.id] = value if isinstance(value, Provenance) else UNKNOWN
            elif not isinstance(node, ast.Expr):
                self.warn(node, "Module-level execution is outside the supported subset")

    def call(self, node: ast.Call, environment: dict[str, Value]) -> Value:
        callee_value = self.expression(node.func, environment)
        callee = callee_value.reference if isinstance(callee_value, Provenance) else None
        contracts = {
            "iomgrp.iomgrp": (("embedding", "key", "config"), {"config": FIXED}),
            "iomgrp.iomgrp_batch": (("embeddings", "key", "config"), {"config": FIXED}),
            "iomgrp.iomgrp_encoded": (("embedding", "key", "config"), {"config": FIXED}),
            "iomgrp.iomgrp_encoded_batch": (("embeddings", "key", "config"), {"config": FIXED}),
            "polyprotect.polyprotect": (("embedding", "key", "config"), {"config": FIXED}),
            "polyprotect.polyprotect_batch": (("embeddings", "key", "config"), {"config": FIXED}),
        }
        if callee not in contracts:
            return super().call(node, environment)
        names, defaults = contracts[callee]
        arguments = self.bind_call(node, environment, names, defaults)
        if arguments is None or not all(isinstance(value, Provenance) for value in arguments):
            return UNKNOWN
        key = arguments[1]
        assert isinstance(key, Provenance)
        self.sink(node, key, callee.split(".", 1)[0], 1.0)
        return UNKNOWN


def analyse_source_v3(source: str, entry: str, record_argument: str = "record_id") -> dict:
    return SourceAnalysisV3(source).analyse(entry, record_argument)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--entry", required=True)
    parser.add_argument("--record-argument", default="record_id")
    args = parser.parse_args()
    print(json.dumps(analyse_source_v3(args.source.read_text(encoding="utf-8"), args.entry, args.record_argument), indent=2))


if __name__ == "__main__":
    main()
