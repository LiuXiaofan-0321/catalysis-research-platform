"""Whitelisted arithmetic DSL for descriptor formulas.

A formula is one Python expression over named numeric inputs, numeric
constants, + - * / ** % //, unary +/-, and the functions listed below. Anything
else (attributes, subscripts, comprehensions, keywords, unknown names) is
rejected before evaluation.
"""
from __future__ import annotations

import ast
import math
from typing import Callable

import numpy as np

MAX_AST_DEPTH = 24

UNARY_FUNCTIONS = {
    "log": np.log, "log10": np.log10, "log2": np.log2, "exp": np.exp,
    "sqrt": np.sqrt, "abs": np.abs, "floor": np.floor, "ceil": np.ceil,
}
BINARY_FUNCTIONS = {
    "minimum": np.minimum, "maximum": np.maximum,
    "min": np.minimum, "max": np.maximum,
}
FUNCTION_WHITELIST = {**UNARY_FUNCTIONS, **BINARY_FUNCTIONS}
CONSTANT_WHITELIST = {"pi": math.pi, "e": math.e}


class DslError(ValueError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(f"{code}: {message}")
        self.code = code


def compile_formula(formula: str, allowed_inputs: set[str]) -> tuple[Callable[[dict[str, np.ndarray]], np.ndarray], set[str]]:
    """Parse and whitelist-check one formula; return an evaluator over env arrays."""
    if not isinstance(formula, str) or not formula.strip():
        raise DslError("schema_invalid", "formula is empty")
    try:
        tree = ast.parse(formula.strip(), mode="eval")
    except SyntaxError as exc:
        raise DslError("schema_invalid", f"not parseable: {exc.msg}") from exc

    used: set[str] = set()

    def visit(node: ast.AST, depth: int) -> None:
        if depth > MAX_AST_DEPTH:
            raise DslError("unsafe_expression", "expression nesting too deep")
        if isinstance(node, ast.Expression):
            visit(node.body, depth + 1)
        elif isinstance(node, ast.BinOp) and isinstance(
            node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv)
        ):
            visit(node.left, depth + 1)
            visit(node.right, depth + 1)
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            visit(node.operand, depth + 1)
        elif isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name) or node.func.id not in FUNCTION_WHITELIST:
                raise DslError("unsafe_expression", "function not in whitelist")
            if node.keywords:
                raise DslError("unsafe_expression", "keyword arguments not allowed")
            arity = 2 if node.func.id in BINARY_FUNCTIONS else 1
            if len(node.args) != arity:
                raise DslError("schema_invalid", f"{node.func.id} expects {arity} argument(s)")
            for argument in node.args:
                visit(argument, depth + 1)
        elif isinstance(node, ast.Name):
            if node.id in CONSTANT_WHITELIST:
                return
            if node.id in allowed_inputs:
                used.add(node.id)
                return
            raise DslError("unsupported_input", f"unknown name: {node.id}")
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return
        else:
            raise DslError("unsafe_expression", f"syntax element {type(node).__name__} not allowed")

    visit(tree, 0)

    def evaluate(env: dict[str, np.ndarray]) -> np.ndarray:
        return _eval_node(tree.body, env)

    return evaluate, used


def _eval_node(node: ast.AST, env: dict[str, np.ndarray]) -> np.ndarray:
    if isinstance(node, ast.Constant):
        return np.float64(node.value)
    if isinstance(node, ast.Name):
        if node.id in CONSTANT_WHITELIST:
            return np.float64(CONSTANT_WHITELIST[node.id])
        return np.asarray(env[node.id], dtype=float)
    if isinstance(node, ast.UnaryOp):
        value = _eval_node(node.operand, env)
        return -value if isinstance(node.op, ast.USub) else +value
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left, env)
        right = _eval_node(node.right, env)
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            if isinstance(node.op, ast.Pow):
                return left ** right
            if isinstance(node.op, ast.Mod):
                return np.mod(left, right)
            return left // right
    if isinstance(node, ast.Call):
        fn = FUNCTION_WHITELIST[node.func.id]
        arguments = [_eval_node(argument, env) for argument in node.args]
        with np.errstate(divide="ignore", invalid="ignore", over="ignore"):
            return fn(*arguments)
    raise DslError("unsafe_expression", "unexpected node during evaluation")
