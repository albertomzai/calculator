"""Blueprint containing API endpoints for the calculator."""

from flask import Blueprint, request, jsonify
import ast

__all__ = ["api_bp"]

api_bp = Blueprint("api", __name__)

def _safe_eval(expr: str):
    """Safely evaluate a mathematical expression.

    Supports +, -, *, / and parentheses. Raises ValueError if the
    expression contains unsupported nodes or syntax errors.
    """
    try:
        node = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError("Invalid expression") from e

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num,
                    ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div,
                    ast.Pow, ast.USub, ast.UAdd, ast.Mod, ast.FloorDiv,
                    ast.LShift, ast.RShift, ast.BitOr, ast.BitAnd, ast.BitXor)

    for n in ast.walk(node):
        if not isinstance(n, allowed_nodes):
            raise ValueError("Unsupported expression")

    # Evaluate the AST safely
    try:
        result = eval(compile(node, filename="<expr>", mode="eval"))
    except Exception as e:
        raise ValueError("Error evaluating expression") from e

    return result

@api_bp.route("/calculate", methods=["POST"])
def calculate():
    """Endpoint that receives a mathematical expression and returns the result.

    Expects JSON payload: {"expression": "5*8-3"}
    Returns JSON: {"result": 37}
    """
    data = request.get_json(silent=True)
    if not data or "expression" not in data:
        return jsonify({"error": "Missing expression"}), 400

    expr = str(data["expression"])
    try:
        result = _safe_eval(expr)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"result": result})