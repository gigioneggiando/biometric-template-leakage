"""Versioned extension of the bounded Python key-provenance interpreter."""
from __future__ import annotations

import argparse
import ast
from dataclasses import asdict, dataclass
import json
from pathlib import Path

from .source_analysis import FIXED, RECORD, UNKNOWN, Provenance, SourceAnalysis


@dataclass(frozen=True)
class SequenceValue:
    items: tuple[object, ...]


@dataclass(frozen=True)
class MappingValue:
    items: tuple[tuple[object, object], ...]


Value = Provenance | SequenceValue | MappingValue


class SourceAnalysisV2(SourceAnalysis):
    """Add conservative control flow, calls, containers and arithmetic to v1."""

    @staticmethod
    def join(values: list[Value]) -> Value:
        if not values:
            return UNKNOWN
        if not all(isinstance(value, Provenance) for value in values):
            return values[0] if all(value == values[0] for value in values) else UNKNOWN
        provenances = [value for value in values if isinstance(value, Provenance)]
        scopes = {value.scope for value in provenances}
        if scopes <= {"fixed", "bounded", "noninjective"}:
            capacities = [value.capacity for value in provenances]
            capacity = sum(capacities) if all(item is not None for item in capacities) else None
            return Provenance("bounded" if capacity is not None else "noninjective", capacity)
        # Two path-local injective summaries need not be injective after paths join.
        if len(provenances) == 1:
            return provenances[0]
        return UNKNOWN

    def expression(self, node: ast.AST, environment: dict[str, Value]) -> Value:
        if isinstance(node, (ast.Tuple, ast.List)):
            return SequenceValue(tuple(self.expression(item, environment) for item in node.elts))
        if isinstance(node, ast.Dict):
            if any(not isinstance(key, ast.Constant) for key in node.keys):
                self.warn(node, "Only dictionaries with literal keys are supported")
                return UNKNOWN
            return MappingValue(
                tuple((key.value, self.expression(value, environment)) for key, value in zip(node.keys, node.values))
            )
        if isinstance(node, ast.Subscript):
            owner = self.expression(node.value, environment)
            index = self.expression(node.slice, environment)
            if isinstance(owner, SequenceValue) and isinstance(index, Provenance) and index.integer is not None:
                if -len(owner.items) <= index.integer < len(owner.items):
                    return owner.items[index.integer]
            if isinstance(owner, MappingValue) and isinstance(index, Provenance):
                mapping = dict(owner.items)
                if index.integer is not None and index.integer in mapping:
                    return mapping[index.integer]
                if index.scope in {"bounded", "noninjective"}:
                    return self.join(list(mapping.values()))
            self.warn(node, "Container selection cannot be resolved safely")
            return UNKNOWN
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Sub) and ast.dump(node.left) == ast.dump(node.right):
                return Provenance("fixed", 1, 0)
            if isinstance(node.op, ast.FloorDiv):
                left = self.expression(node.left, environment)
                right = self.expression(node.right, environment)
                if not isinstance(left, Provenance) or not isinstance(right, Provenance):
                    self.warn(node, "Floor-division operands are unresolved")
                    return UNKNOWN
                if left.integer is not None and right.integer not in {None, 0}:
                    return Provenance("fixed", 1, left.integer // right.integer)
                if left.scope == "record_injective" and right.integer is not None and abs(right.integer) > 1:
                    return Provenance("noninjective")
                self.warn(node, "Floor division is not proven injective")
                return UNKNOWN
        if isinstance(node, ast.Call):
            return self.call(node, environment)
        return super().expression(node, environment)  # type: ignore[arg-type]

    def bind_call(
        self,
        node: ast.Call,
        environment: dict[str, Value],
        names: tuple[str, ...],
        defaults: dict[str, Value] | None = None,
    ) -> list[Value] | None:
        if len(node.args) > len(names) or any(keyword.arg is None for keyword in node.keywords):
            self.warn(node, "Expanded or excessive call arguments are unsupported")
            return None
        bound = {name: self.expression(value, environment) for name, value in zip(names, node.args)}
        for keyword in node.keywords:
            if keyword.arg not in names or keyword.arg in bound:
                self.warn(node, "Unknown or duplicate keyword argument")
                return None
            bound[keyword.arg] = self.expression(keyword.value, environment)
        for name, value in (defaults or {}).items():
            bound.setdefault(name, value)
        if any(name not in bound for name in names):
            self.warn(node, "Required call argument is missing")
            return None
        return [bound[name] for name in names]

    def call(self, node: ast.Call, environment: dict[str, Value]) -> Value:
        callee_value = self.expression(node.func, environment)
        callee = callee_value.reference if isinstance(callee_value, Provenance) else None
        if callee == "numpy.concatenate":
            if len(node.args) != 1 or not isinstance(node.args[0], (ast.List, ast.Tuple)):
                self.warn(node, "Concatenation requires an explicit sequence")
                return UNKNOWN
            axis = next((item.value for item in node.keywords if item.arg == "axis"), None)
            if len(node.keywords) != 1 or not isinstance(axis, ast.Constant) or axis.value != 1:
                self.warn(node, "Only explicit axis=1 concatenation is supported")
                return UNKNOWN
            arrays = [self.expression(item, environment) for item in node.args[0].elts]
            if arrays and all(isinstance(array, Provenance) and array.blocks for array in arrays):
                return Provenance(blocks=tuple(block for array in arrays for block in array.blocks))
            self.warn(node, "Concatenated projection blocks are unresolved")
            return UNKNOWN
        if callee and callee.startswith("local."):
            function = self.functions[callee.removeprefix("local.")]
            names = tuple(argument.arg for argument in function.args.posonlyargs + function.args.args)
            arguments = self.bind_call(node, environment, names)
            return self.function(callee.removeprefix("local."), arguments) if arguments is not None else UNKNOWN

        contracts = {
            "biohash.generate_key": (("master_seed", "split", "index"), {}),
            "biohash._orthonormal_projection": (
                ("input_dim", "output_dim", "key", "haar_sign_corrected"),
                {"haar_sign_corrected": FIXED},
            ),
            "biohash.biohash": (("embedding", "key", "config"), {"config": FIXED}),
            "biohash.biohash_batch": (("embeddings", "key", "config"), {"config": FIXED}),
            "biohash.correlated_biohash": (
                ("embedding", "shared_key", "private_key", "shared_dimensions", "config"),
                {"config": FIXED},
            ),
        }
        if callee not in contracts:
            self.warn(node, "Call has no verified key/projection summary")
            return UNKNOWN
        names, defaults = contracts[callee]
        arguments = self.bind_call(node, environment, names, defaults)
        if arguments is None or not all(isinstance(value, Provenance) for value in arguments):
            return UNKNOWN
        values = [value for value in arguments if isinstance(value, Provenance)]
        if callee == "biohash.generate_key":
            if any(value.scope == "unknown" for value in values):
                self.warn(node, "Unknown key derivation input")
                return UNKNOWN
            if any(value.scope == "noninjective" for value in values):
                return Provenance("noninjective")
            if sum(value.scope == "record_injective" for value in values) == 1 and all(
                value.scope in {"fixed", "record_injective"} for value in values
            ):
                return RECORD
            if all(value.scope == "fixed" for value in values):
                return FIXED
            if all(value.capacity is not None for value in values):
                capacity = 1
                for value in values:
                    capacity *= value.capacity
                return Provenance("bounded", capacity)
            self.warn(node, "Joint key-input dependence is outside the injectivity contract")
            return UNKNOWN
        if callee == "biohash._orthonormal_projection":
            width = values[1].integer
            if width is not None and width > 0:
                key = values[2]
                return Provenance(blocks=((width, key.scope, key.capacity),))
            self.warn(node, "Projection width must be a known positive integer")
            return UNKNOWN
        if callee in {"biohash.biohash", "biohash.biohash_batch"}:
            self.sink(node, values[1], "whole", 1.0)
            return UNKNOWN
        shared = values[3].integer
        if shared is None or shared < 0:
            self.warn(node, "Shared projection width is not a known nonnegative integer")
        elif shared > 0:
            self.sink(node, values[1], "shared_prefix", None)
        self.sink(node, values[2], "private_suffix", None)
        return UNKNOWN

    def sink(self, node: ast.AST, key: Provenance, component: str, weight: float | None) -> None:
        self.sinks.append(
            {"line": node.lineno, "component": component, "weight": weight, "key": asdict(key),
             "trace": list(self.active)}
        )
        if key.scope in {"fixed", "bounded", "noninjective"}:
            suffix = f", capacity <= {key.capacity}" if key.capacity is not None else ""
            self.findings.append(
                {"rule": "IMPLEMENTATION_REUSE", "line": node.lineno,
                 "message": f"{component}: {key.scope} key provenance{suffix}"}
            )
        elif key.scope == "unknown":
            self.warn(node, "Protection sink receives unresolved key provenance")

    def execute_block(
        self, statements: list[ast.stmt], environment: dict[str, Value]
    ) -> tuple[dict[str, Value], Value | None, bool]:
        current = dict(environment)
        for statement in statements:
            if isinstance(statement, ast.Assign) and all(isinstance(target, ast.Name) for target in statement.targets):
                value = self.expression(statement.value, current)
                for target in statement.targets:
                    current[target.id] = value
            elif isinstance(statement, ast.Return):
                return current, self.expression(statement.value, current) if statement.value else UNKNOWN, True
            elif isinstance(statement, ast.Expr):
                self.expression(statement.value, current)
            elif isinstance(statement, ast.If):
                predicate_nodes = (
                    ast.Name, ast.Load, ast.Constant, ast.BinOp, ast.Mod, ast.BitAnd,
                    ast.Add, ast.Sub, ast.Mult, ast.FloorDiv, ast.Compare, ast.Eq,
                    ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.BoolOp, ast.And,
                    ast.Or, ast.UnaryOp, ast.Not, ast.USub, ast.UAdd,
                )
                if any(not isinstance(node, predicate_nodes) for node in ast.walk(statement.test)):
                    self.warn(statement.test, "Branch condition has unsupported execution or side effects")
                sink_count = len(self.sinks)
                then_environment, then_value, then_returned = self.execute_block(statement.body, current)
                else_environment, else_value, else_returned = self.execute_block(statement.orelse, current)
                if len(self.sinks) != sink_count:
                    self.warn(statement, "Branch-local protection calls require cross-path key analysis")
                if then_returned or else_returned:
                    if then_returned and else_returned:
                        return current, self.join([then_value or UNKNOWN, else_value or UNKNOWN]), True
                    self.warn(statement, "Only branches with matching return behavior are supported")
                    return current, UNKNOWN, True
                keys = set(current) | set(then_environment) | set(else_environment)
                current = {
                    key: self.join([then_environment.get(key, current.get(key, UNKNOWN)),
                                    else_environment.get(key, current.get(key, UNKNOWN))])
                    for key in keys
                }
            elif isinstance(statement, ast.For):
                sequence = self.expression(statement.iter, current)
                if (not isinstance(statement.target, ast.Name) or not isinstance(sequence, SequenceValue)
                        or statement.orelse):
                    self.warn(statement, "Only finite literal loops with a name target are supported")
                    return current, UNKNOWN, True
                for item in sequence.items:
                    current[statement.target.id] = item
                    current, value, returned = self.execute_block(statement.body, current)
                    if returned:
                        self.warn(statement, "Returns inside unrolled loops are unsupported")
                        return current, value, True
            else:
                self.warn(statement, f"Unsupported statement: {type(statement).__name__}")
                return current, UNKNOWN, True
        return current, None, False

    def function(self, name: str, arguments: list[Value]) -> Value:
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
            _, value, returned = self.execute_block(node.body, environment)
            return value if returned and value is not None else UNKNOWN
        finally:
            self.active.pop()


def analyse_source_v2(source: str, entry: str, record_argument: str = "record_id") -> dict:
    return SourceAnalysisV2(source).analyse(entry, record_argument)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--entry", required=True)
    parser.add_argument("--record-argument", default="record_id")
    args = parser.parse_args()
    print(json.dumps(analyse_source_v2(args.source.read_text(encoding="utf-8"), args.entry, args.record_argument), indent=2))


if __name__ == "__main__":
    main()
