"""Blueprint containing the API endpoints for calculation."""

import ast
from flask import Blueprint, request, jsonify, abort

__all__ = ["bp"]

bp = Blueprint('api', __name__, url_prefix='/api')

def _safe_eval(expr: str):
    """Evaluate a mathematical expression safely.

    Only allows numbers and the operators +, -, *, /, **, //, % and parentheses.
    Args:
        expr (str): The expression to evaluate.
    Returns:
        float or int: The result of the evaluation.
    Raises:
        ValueError: If the expression contains disallowed nodes.
    """
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError("Invalid syntax") from e

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant, ast.operator, ast.unaryop)
    for subnode in ast.walk(node):
        if not isinstance(subnode, allowed_nodes):
            raise ValueError("Disallowed expression")

    # Use eval with empty globals and locals to prevent access to builtins
    try:
        result = eval(compile(node, '<string>', 'eval'), {}, {})
    except Exception as e:
        raise ValueError("Evaluation error") from e

    return result

@bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression.

    Expects JSON payload: {"expression": "5*8-3"}
    Returns:
        JSON: {"result": 37}
    """
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    expression = data.get('expression')
    if not isinstance(expression, str):
        abort(400, description="'expression' must be a string")

    try:
        result = _safe_eval(expression)
    except ValueError as e:
        abort(400, description=str(e))

    return jsonify({"result": result})