"""Utility functions for the calculator backend."""

import ast

_ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.FloorDiv,
    ast.UAdd, ast.USub
}

def _eval(node):
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif hasattr(ast, 'Constant') and isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
    elif isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type is ast.Add:
            return left + right
        elif op_type is ast.Sub:
            return left - right
        elif op_type is ast.Mult:
            return left * right
        elif op_type is ast.Div:
            return left / right
        elif op_type is ast.Pow:
            return left ** right
        elif op_type is ast.Mod:
            return left % right
        elif op_type is ast.FloorDiv:
            return left // right
    elif isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        operand = _eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
    raise ValueError('Unsupported expression')

def safe_eval(expr: str):
    """Safely evaluate a mathematical expression containing only basic operators."""
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError('Syntax error') from e

    if not isinstance(parsed.body, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num)) and not hasattr(ast, 'Constant'):  # pragma: no cover
        raise ValueError('Unsupported expression type')

    return _eval(parsed.body)