"""Bounded, contract-based abstract interpretation of Python key provenance."""
from __future__ import annotations

import argparse
import ast
from dataclasses import asdict, dataclass
import json
from pathlib import Path


@dataclass(frozen=True)
class Provenance:
    scope: str = "unknown"
    capacity: int | None = None
    integer: int | None = None
    reference: str | None = None
    blocks: tuple[tuple[int, str, int | None], ...] = ()


UNKNOWN = Provenance()
FIXED = Provenance("fixed", 1)
RECORD = Provenance("record_injective")
KEY_MODULES = {"biometrics_ai.protection", "biometrics_ai.protection.biohash"}


class SourceAnalysis:
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
            elif isinstance(node, ast.ImportFrom) and node.module in KEY_MODULES:
                for alias in node.names:
                    self.globals[alias.asname or alias.name] = Provenance(reference=f"biohash.{alias.name}")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in KEY_MODULES and alias.asname:
                        self.globals[alias.asname] = Provenance(reference="biohash")
                    elif alias.name == "numpy":
                        self.globals[alias.asname or "numpy"] = Provenance(reference="numpy")
                    else:
                        self.globals[alias.asname or alias.name.split(".")[0]] = UNKNOWN
            elif isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    self.globals[alias.asname or alias.name] = UNKNOWN
            elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.globals[target.id] = self.expression(node.value, {})
            elif not isinstance(node, (ast.ImportFrom, ast.Expr)):
                self.warn(node, "Module-level execution is outside the supported subset")

    def warn(self, node: ast.AST, message: str) -> None:
        finding = {"rule": "UNSUPPORTED", "line": getattr(node, "lineno", 0), "message": message}
        if finding not in self.findings:
            self.findings.append(finding)

    def expression(self, node: ast.AST, environment: dict[str, Provenance]) -> Provenance:
        if isinstance(node, ast.Constant):
            return Provenance("fixed", 1, node.value if type(node.value) is int else None)
        if isinstance(node, ast.Name):
            if node.id in environment:
                return environment[node.id]
            return self.globals.get(node.id, UNKNOWN)
        if isinstance(node, ast.Attribute):
            owner = self.expression(node.value, environment)
            if owner.reference in {"biohash", "numpy"}:
                return Provenance(reference=f"{owner.reference}.{node.attr}")
            return UNKNOWN
        if isinstance(node, ast.Compare) and len(node.ops) == 1 and isinstance(node.ops[0], ast.GtE):
            projected = self.expression(node.left, environment)
            threshold = self.expression(node.comparators[0], environment)
            if projected.blocks and threshold.integer == 0:
                total = sum(block[0] for block in projected.blocks)
                for index, (width, scope, capacity) in enumerate(projected.blocks):
                    self.sink(node, Provenance(scope, capacity), f"matrix_block_{index}", width / total)
                return UNKNOWN
            self.warn(node, "Only zero-threshold comparisons of modeled projection blocks are summarized")
            return UNKNOWN
        if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.USub, ast.UAdd)):
            value = self.expression(node.operand, environment)
            if value.integer is not None:
                integer = -value.integer if isinstance(node.op, ast.USub) else value.integer
                return Provenance("fixed", 1, integer)
            return value if value.scope == "record_injective" else UNKNOWN
        if isinstance(node, ast.BinOp):
            left = self.expression(node.left, environment)
            right = self.expression(node.right, environment)
            if isinstance(node.op, ast.MatMult) and right.blocks and left.scope == "fixed":
                return right
            if isinstance(node.op, ast.Mod) and right.integer is not None and right.integer > 0:
                if left.integer is not None:
                    return Provenance("fixed", 1, left.integer % right.integer)
                if left.scope != "unknown":
                    return Provenance("bounded", right.integer)
            if isinstance(node.op, ast.BitAnd) and right.integer is not None and right.integer >= 0:
                if left.integer is not None:
                    return Provenance("fixed", 1, left.integer & right.integer)
                if left.scope != "unknown":
                    return Provenance("bounded", 2 ** right.integer.bit_count())
            if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult)):
                if left.integer is not None and right.integer is not None:
                    integer = (left.integer + right.integer if isinstance(node.op, ast.Add) else
                               left.integer - right.integer if isinstance(node.op, ast.Sub) else left.integer * right.integer)
                    return Provenance("fixed", 1, integer)
                variable, constant = (left, right) if right.integer is not None else (right, left)
                if constant.integer is not None:
                    if isinstance(node.op, ast.Mult) and constant.integer == 0:
                        return Provenance("fixed", 1, 0)
                    if variable.scope in {"record_injective", "bounded", "fixed"}:
                        return Provenance(variable.scope, variable.capacity)
            self.warn(node, "Unsupported arithmetic; record dependence alone does not prove freshness")
            return UNKNOWN
        if isinstance(node, ast.Call):
            callee = self.expression(node.func, environment).reference
            if callee == "numpy.concatenate" and len(node.args) == 1 and isinstance(node.args[0], (ast.List, ast.Tuple)):
                if (len(node.keywords) == 1 and node.keywords[0].arg == "axis"
                        and isinstance(node.keywords[0].value, ast.Constant) and node.keywords[0].value.value == 1):
                    arrays = [self.expression(item, environment) for item in node.args[0].elts]
                    if arrays and all(array.blocks for array in arrays):
                        return Provenance(blocks=tuple(block for array in arrays for block in array.blocks))
                self.warn(node, "Only explicit axis=1 concatenation of modeled projection blocks is supported")
                return UNKNOWN
            arguments = [self.expression(argument, environment) for argument in node.args]
            if node.keywords:
                self.warn(node, "Keyword/expanded arguments require an explicit call contract")
                return UNKNOWN
            if callee and callee.startswith("local."):
                return self.function(callee.removeprefix("local."), arguments)
            if callee == "biohash._orthonormal_projection" and len(arguments) == 4:
                width = arguments[1].integer
                if width is not None and width > 0:
                    key = arguments[2]
                    return Provenance(blocks=((width, key.scope, key.capacity),))
                self.warn(node, "Projection width must be a known positive integer")
                return UNKNOWN
            if callee == "biohash.generate_key" and len(arguments) == 3:
                if any(value.scope == "unknown" for value in arguments):
                    self.warn(node, "Unknown key derivation input")
                    return UNKNOWN
                if sum(value.scope == "record_injective" for value in arguments) == 1 and all(
                        value.scope in {"fixed", "record_injective"} for value in arguments):
                    return RECORD
                if all(value.scope == "fixed" for value in arguments):
                    return FIXED
                if all(value.capacity is not None for value in arguments):
                    capacity = 1
                    for value in arguments:
                        capacity *= value.capacity
                    return Provenance("bounded", capacity)
                self.warn(node, "Joint key-input dependence is outside the injectivity contract")
                return UNKNOWN
            if callee in {"biohash.biohash", "biohash.biohash_batch"} and len(arguments) == 3:
                self.sink(node, arguments[1], "whole", 1.0)
                return UNKNOWN
            if callee == "biohash.correlated_biohash" and len(arguments) == 5:
                shared = arguments[3].integer
                if shared is None or shared < 0:
                    self.warn(node, "Shared projection width is not a known nonnegative integer")
                elif shared > 0:
                    self.sink(node, arguments[1], "shared_prefix", None)
                self.sink(node, arguments[2], "private_suffix", None)
                return UNKNOWN
            self.warn(node, "Call has no verified key/projection summary")
            return UNKNOWN
        self.warn(node, f"Unsupported expression: {type(node).__name__}")
        return UNKNOWN

    def sink(self, node: ast.AST, key: Provenance, component: str, weight: float | None) -> None:
        self.sinks.append({"line": node.lineno, "component": component, "weight": weight,
                           "key": asdict(key), "trace": list(self.active)})
        if key.scope in {"fixed", "bounded"}:
            self.findings.append({"rule": "IMPLEMENTATION_REUSE", "line": node.lineno,
                                  "message": f"{component}: {key.scope} key provenance, capacity <= {key.capacity}"})
        elif key.scope == "unknown":
            self.warn(node, "Protection sink receives unresolved key provenance")

    def function(self, name: str, arguments: list[Provenance]) -> Provenance:
        node = self.functions[name]
        if name in self.active or len(self.active) >= 16:
            self.warn(node, "Recursion/depth limit")
            return UNKNOWN
        if (node.decorator_list or node.args.defaults or node.args.kwonlyargs or node.args.vararg
                or node.args.kwarg or len(node.args.posonlyargs + node.args.args) != len(arguments)):
            self.warn(node, "Unsupported function signature or decorators")
            return UNKNOWN
        environment = dict(zip([argument.arg for argument in node.args.posonlyargs + node.args.args], arguments))
        self.active.append(name)
        try:
            for statement in node.body:
                if isinstance(statement, ast.Assign) and all(isinstance(target, ast.Name) for target in statement.targets):
                    value = self.expression(statement.value, environment)
                    for target in statement.targets:
                        environment[target.id] = value
                elif isinstance(statement, ast.Return):
                    return self.expression(statement.value, environment) if statement.value else UNKNOWN
                elif isinstance(statement, ast.Expr):
                    self.expression(statement.value, environment)
                else:
                    self.warn(statement, f"Unsupported statement: {type(statement).__name__}")
                    return UNKNOWN
        finally:
            self.active.pop()
        return UNKNOWN

    def analyse(self, entry: str, record_argument: str) -> dict:
        if entry not in self.functions:
            raise ValueError(f"Unknown entry function: {entry}")
        node = self.functions[entry]
        names = [argument.arg for argument in node.args.posonlyargs + node.args.args]
        if record_argument not in names:
            raise ValueError("Record argument must be an entry parameter")
        if self.globals.get(entry, UNKNOWN).reference != f"local.{entry}":
            self.warn(node, "Entry function was rebound at module scope")
        else:
            self.function(entry, [RECORD if name == record_argument else FIXED for name in names])
        if not self.sinks:
            self.warn(node, "No modeled protection sink reached")
        reuse = any(finding["rule"] == "IMPLEMENTATION_REUSE" for finding in self.findings)
        unresolved = any(finding["rule"] == "UNSUPPORTED" for finding in self.findings)
        return {"entry": entry, "record_argument": record_argument,
                "decision": "reuse" if reuse else "unknown" if unresolved else "conditional_fresh",
                "complete": not unresolved, "sinks": self.sinks, "findings": self.findings,
                "assumptions": "Integer record IDs are unique; other inputs fixed in audited context; trusted unmodified "
                "callee contracts; ideal collision-free KDF; no reflection, monkeypatching or external state mutation. "
                "Freshness is not secrecy, independence, unlinkability or a deployment approval."}


def analyse_source(source: str, entry: str, record_argument: str = "record_id") -> dict:
    return SourceAnalysis(source).analyse(entry, record_argument)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--entry", required=True)
    parser.add_argument("--record-argument", default="record_id")
    args = parser.parse_args()
    print(json.dumps(analyse_source(args.source.read_text(encoding="utf-8"), args.entry, args.record_argument), indent=2))


if __name__ == "__main__":
    main()