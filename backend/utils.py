# backend/utils.py

import ast
import operator

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}

def _eval(node):
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if hasattr(ast, 'Constant') and isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError('Unsupported constant type')

    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left = _eval(node.left)
        right = _eval(node.right)
        return _OPERATORS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        operand = _eval(node.operand)
        return _OPERATORS[type(node.op)](operand)

    raise ValueError('Unsupported expression')

def safe_eval(expr: str):
    """Safely evaluate a basic arithmetic expression.

    Supports +, -, *, /, parentheses and unary minus.
    Raises ValueError if the expression contains disallowed nodes."""
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError('Syntax error in expression') from e

    return _eval(tree.body)