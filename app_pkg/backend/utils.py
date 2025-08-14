# app_pkg.backend.utils

import ast

_ALLOWED_OPERATORS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
    ast.UAdd
}

def _eval(node):
    if isinstance(node, ast.Num):  # < Python3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError('Unsupported constant type')

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type is ast.Add:
            return left + right
        if op_type is ast.Sub:
            return left - right
        if op_type is ast.Mult:
            return left * right
        if op_type is ast.Div:
            return left / right
        if op_type is ast.Pow:
            return left ** right

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        operand = _eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand

    raise ValueError('Unsupported expression')

def safe_eval(expr: str):
    """Evaluate a mathematical expression safely.

    Only arithmetic operators are allowed. Raises ``ValueError`` if the
    expression contains disallowed nodes.
    """
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError('Invalid syntax') from e

    if not isinstance(tree.body, (ast.Expression, ast.BinOp, ast.UnaryOp)):
        raise ValueError('Expression must be a single arithmetic expression')

    return _eval(tree.body)