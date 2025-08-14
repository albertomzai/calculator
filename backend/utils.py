# Utility functions for safe evaluation of arithmetic expressions

import ast

def _is_valid_node(node):
    """Recursively ensure that the AST node contains only allowed operations."""
    if isinstance(node, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant, ast.Load, ast.operator, ast.unaryop)):
        return True

    # Allowed operators: + - * /
    allowed_ops = {ast.Add, ast.Sub, ast.Mult, ast.Div}
    if isinstance(node, ast.BinOp) and type(node.op) in allowed_ops:
        return _is_valid_node(node.left) and _is_valid_node(node.right)

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        return _is_valid_node(node.operand)

    # Numbers
    if isinstance(node, (ast.Num, ast.Constant)):
        return True

    return False

def safe_eval_expression(expr: str):
    """Evaluate a simple arithmetic expression safely.

    Supports +, -, *, / and integer/float literals only.
    Raises ValueError if the expression is invalid or contains disallowed nodes."""
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError('Syntax error in expression') from e

    # Validate AST structure
    if not _is_valid_node(parsed.body):
        raise ValueError('Expression contains disallowed operations')

    # Use eval with empty globals and locals to compute the result
    try:
        return eval(compile(parsed, '<string>', 'eval'), {}, {})
    except Exception as e:
        raise ValueError('Error evaluating expression') from e