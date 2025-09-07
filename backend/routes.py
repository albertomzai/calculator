"""Blueprint defining the API routes for calculation."""

from flask import Blueprint, request, jsonify
import ast

__all__ = ["bp"]

bp = Blueprint("api", __name__, url_prefix="/api")

def _safe_eval(expr: str):
    """Evaluate a simple mathematical expression safely.

    Only allows numbers and the operators +, -, *, /, **, //, % and parentheses.
    Args:
        expr (str): The expression string to evaluate.
    Returns:
        float: Result of the evaluation.
    Raises:
        ValueError: If the expression contains disallowed nodes.
    """
    allowed_nodes = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Num,
        ast.Constant,  # for Python 3.8+
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.FloorDiv,
        ast.USub,
        ast.UAdd,
        ast.LParen,  # not a real node but placeholder for readability
    }

    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid expression") from exc

    for node in ast.walk(parsed):
        if type(node) not in allowed_nodes:
            raise ValueError(f"Disallowed expression: {type(node).__name__}")

    # Use eval with empty globals and locals to avoid access to builtins
    return eval(compile(parsed, filename="<expr>", mode="eval"), {}, {})

@bp.route("/calculate", methods=["POST"])
def calculate():
    """Endpoint to evaluate a mathematical expression sent in JSON.

    Expected payload: {"expression": "5*8-3"}
    Returns: JSON with key 'result'.
    """
    data = request.get_json(force=True) or {}
    expr = data.get("expression", "")

    if not expr:
        return jsonify({"error": "No expression provided"}), 400

    try:
        result = _safe_eval(expr)
    except Exception as exc:
        return jsonify({"error": str(exc)}), 400

    return jsonify({"result": result})