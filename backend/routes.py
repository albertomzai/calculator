"""Routes for the calculator API."""

import ast
from flask import Blueprint, request, jsonify, abort

__all__ = ["api_bp"]

# Blueprint definition
api_bp = Blueprint('api', __name__, url_prefix='/api')

def _safe_eval(expr: str):
    """Evaluate a mathematical expression safely.

    Only numeric literals and the operators +, -, *, / are allowed.
    Parameters:
        expr (str): The expression string to evaluate.
    Returns:
        float: Result of the evaluated expression.
    Raises:
        ValueError: If the expression contains disallowed nodes.
    """
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError("Invalid syntax") from e

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub)

    for subnode in ast.walk(node):
        if not isinstance(subnode, allowed_nodes):
            raise ValueError("Disallowed expression")

    try:
        result = eval(compile(node, '<string>', 'eval'), {}, {})
    except ZeroDivisionError as e:
        raise ValueError("Division by zero") from e
    return result

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression.

    Expects JSON payload: {"expression": "5*8-3"}
    Returns:
        JSON with key 'result' containing the numeric result.
    """
    data = request.get_json(silent=True)
    if not data or 'expression' not in data:
        abort(400, description="Missing 'expression' field")

    expr = data['expression']
    if not isinstance(expr, str) or not expr.strip():
        abort(400, description="Expression must be a non-empty string")

    try:
        result = _safe_eval(expr)
    except ValueError as e:
        abort(400, description=str(e))

    return jsonify({"result": result})