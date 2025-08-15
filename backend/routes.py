"""Blueprint that exposes the calculation API endpoint."""

import ast
from flask import Blueprint, request, jsonify, abort

api_bp = Blueprint("api", __name__, url_prefix="/api")

def _evaluate_expression(expr: str):
    """Safely evaluate a mathematical expression.

    Only numeric literals and the operators + - * / are allowed. The
    evaluation is performed using Python's AST module to prevent execution of
    arbitrary code.
    """
    try:
        node = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid syntax") from exc

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num,
                     ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div,
                     ast.UAdd, ast.USub)

    for n in ast.walk(node):
        if not isinstance(n, allowed_nodes):
            raise ValueError("Disallowed expression")

    # Evaluate the AST safely using eval with an empty namespace
    try:
        result = eval(compile(node, filename="<expr>", mode="eval"), {}, {})
    except ZeroDivisionError as exc:
        raise ValueError("Division by zero") from exc

    return result

@api_bp.route("/calculate", methods=["POST"])
def calculate():
    """Endpoint that receives a JSON payload with an 'expression' key.

    Returns the evaluated numeric result in JSON format. If the request is
 malformed or the expression cannot be safely evaluated, a 400 error is
 returned with an explanatory message.
    """
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    expression = data.get("expression")

    if not isinstance(expression, str):
        abort(400, description="'expression' must be a string")

    try:
        result = _evaluate_expression(expression)
    except ValueError as exc:
        abort(400, description=str(exc))

    return jsonify({"result": result})