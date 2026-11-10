"""Small allowlisted alternatives to evaluating model-supplied Python."""

import ast
import json
import math
import operator


def arithmetic(expression):
    if not isinstance(expression, str) or not 0 < len(expression) <= 500:
        raise ValueError("Arithmetic expression must contain 1–500 characters")
    try:
        tree = ast.parse(expression, mode="eval")
    except (SyntaxError, RecursionError):
        raise ValueError("Invalid arithmetic expression") from None
    if sum(1 for _ in ast.walk(tree)) > 64:
        raise ValueError("Arithmetic expression is too complex")
    binary = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
    }

    def visit(node, depth=0):
        if depth > 12:
            raise ValueError("Arithmetic nesting budget exceeded")
        if isinstance(node, ast.Constant) and type(node.value) in {int, float}:
            value = node.value
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
            value = visit(node.operand, depth + 1) * (-1 if isinstance(node.op, ast.USub) else 1)
        elif isinstance(node, ast.BinOp) and type(node.op) in binary:
            left, right = visit(node.left, depth + 1), visit(node.right, depth + 1)
            if isinstance(node.op, ast.Pow) and (abs(right) > 10 or (left == 0 and right < 0)):
                raise ValueError("Exponent exceeds the arithmetic budget")
            try:
                value = binary[type(node.op)](left, right)
            except (ArithmeticError, ValueError):
                raise ValueError("Invalid arithmetic operation") from None
        else:
            raise ValueError("Only numeric constants and arithmetic operators are allowed")
        if type(value) not in {int, float} or abs(value) > 1e12 or not math.isfinite(value):
            raise ValueError("Arithmetic magnitude budget exceeded")
        return value

    return visit(tree.body)


def parse_tool_selection(value):
    if not isinstance(value, str) or len(value) > 12000:
        raise ValueError("Tool selection must be bounded JSON text")
    try:
        choice = json.loads(value)
    except (ValueError, RecursionError):
        raise ValueError("Tool selection must be a JSON object") from None
    if not isinstance(choice, dict) or set(choice) != {"tool", "input"}:
        raise ValueError("Tool selection requires exactly tool and input")
    if not isinstance(choice["tool"], str) or choice["tool"] not in {
        "none",
        "calculator_tool",
        "vector_search_tool",
    }:
        raise ValueError("Unknown tool")
    if (
        not isinstance(choice["input"], str)
        or not choice["input"].strip()
        or len(choice["input"]) > 8000
    ):
        raise ValueError("Tool input must be bounded nonempty text")
    return choice["tool"], choice["input"]
