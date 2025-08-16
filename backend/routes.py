# backend/routes.py

import ast
from flask import Blueprint, request, jsonify, abort

api_bp = Blueprint("api", __name__, url_prefix="/api")

def _safe_eval(expr: str):
    """Evaluate a simple arithmetic expression safely using AST."""
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError("Invalid syntax") from e

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,)
    for n in ast.walk(node):
        if not isinstance(n, allowed_nodes) and not isinstance(n, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd, ast.Mod, ast.FloorDiv)):
            raise ValueError("Unsupported expression")

    try:
        return eval(compile(node, '<string>', mode='eval'))
    except Exception as e:
        raise ValueError("Evaluation error") from e

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint that receives a JSON payload with an 'expression' key and returns the evaluated result."""
    if not request.is_json:
        abort(400, description="Request must be in JSON format")

    data = request.get_json()
    expression = data.get('expression')

    if not isinstance(expression, str) or not expression.strip():
        abort(400, description="'expression' must be a non-empty string")

    try:
        result = _safe_eval(expression)
    except ValueError as e:
        abort(400, description=str(e))

    return jsonify({'result': result})