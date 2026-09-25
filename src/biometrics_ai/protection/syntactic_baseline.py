"""Simple intraprocedural AST baseline for protection-key provenance."""
from __future__ import annotations

import ast


SINKS = {
    "biohash", "biohash_batch", "iomgrp", "iomgrp_batch", "iomgrp_encoded",
    "iomgrp_encoded_batch", "polyprotect", "polyprotect_batch",
}


def analyse_syntax(source: str, entry: str, record_argument: str = "record_id") -> dict:
    tree = ast.parse(source)
    functions = {node.name: node for node in tree.body if isinstance(node, ast.FunctionDef)}
    if entry not in functions:
        raise ValueError(f"Unknown entry function: {entry}")
    aliases = {}
    for node in tree.body:
        if isinstance(node, ast.ImportFrom):
            aliases.update({alias.asname or alias.name: alias.name for alias in node.names})
    function = functions[entry]
    names = [argument.arg for argument in function.args.posonlyargs + function.args.args]
    environment = {name: "fresh" if name == record_argument else "fixed" for name in names}
    calls = []

    def call_name(node: ast.Call) -> str | None:
        name = node.func.id if isinstance(node.func, ast.Name) else node.func.attr if isinstance(node.func, ast.Attribute) else None
        return aliases.get(name, name) if name else None

    def origin(node: ast.AST) -> str:
        if isinstance(node, ast.Constant):
            return "fixed"
        if isinstance(node, ast.Name):
            return environment.get(node.id, "unknown")
        if isinstance(node, ast.UnaryOp):
            return origin(node.operand)
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Sub) and ast.dump(node.left) == ast.dump(node.right):
                return "fixed"
            left, right = origin(node.left), origin(node.right)
            if isinstance(node.op, (ast.Mod, ast.BitAnd, ast.FloorDiv)):
                return "reuse" if left in {"fresh", "reuse"} and right == "fixed" else "unknown"
            if isinstance(node.op, (ast.Add, ast.Sub, ast.Mult)):
                if left == right == "fixed":
                    return "fixed"
                if {left, right} == {"fresh", "fixed"}:
                    return "fresh"
                if "reuse" in {left, right} and "unknown" not in {left, right}:
                    return "reuse"
            return "unknown"
        if isinstance(node, ast.Call) and call_name(node) == "generate_key":
            values = [origin(argument) for argument in node.args]
            values.extend(origin(keyword.value) for keyword in node.keywords if keyword.arg is not None)
            if len(values) != 3:
                return "unknown"
            if values.count("fresh") == 1 and all(value in {"fresh", "fixed"} for value in values):
                return "fresh"
            if all(value == "fixed" for value in values):
                return "fixed"
            if "reuse" in values and "unknown" not in values:
                return "reuse"
        return "unknown"

    def inspect_sink(node: ast.AST) -> None:
        if not isinstance(node, ast.Call) or call_name(node) not in SINKS:
            return
        key = node.args[1] if len(node.args) > 1 else next(
            (keyword.value for keyword in node.keywords if keyword.arg == "key"), None
        )
        provenance = origin(key) if key is not None else "unknown"
        decision = "conditional_fresh" if provenance == "fresh" else "reuse" if provenance in {"fixed", "reuse"} else "unknown"
        calls.append({"line": node.lineno, "sink": call_name(node), "decision": decision})

    unsupported = False
    for statement in function.body:
        if isinstance(statement, ast.Assign) and all(isinstance(target, ast.Name) for target in statement.targets):
            value = origin(statement.value)
            for target in statement.targets:
                environment[target.id] = value
        elif isinstance(statement, ast.Return):
            inspect_sink(statement.value)
        elif isinstance(statement, ast.Expr):
            inspect_sink(statement.value)
        else:
            unsupported = True
            break
    decisions = {call["decision"] for call in calls}
    decision = (
        "reuse" if "reuse" in decisions else
        "conditional_fresh" if decisions == {"conditional_fresh"} and not unsupported else
        "unknown"
    )
    return {
        "entry": entry,
        "decision": decision,
        "complete": decision != "unknown",
        "calls": calls,
        "scope": "single function; no helpers, branches, loops, containers or component contracts",
    }
