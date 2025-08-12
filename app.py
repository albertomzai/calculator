# app.py
"""Flask application for a secure calculator API.

This module defines the Flask app, configures CORS, and exposes a single POST endpoint
`/api/calculate`. The calculation logic is implemented in a helper function that
parses the incoming mathematical expression using Python's `ast` module to avoid
executing arbitrary code.  The API returns JSON responses with appropriate HTTP
status codes for success or error conditions.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import ast

app = Flask(__name__)
# Enable CORS to allow the frontend SPA to make requests from a different origin
CORS(app)

# ---------------------------------------------------------------------------
# Helper: Safe expression evaluator
# ---------------------------------------------------------------------------
class EvalError(Exception):
    """Custom exception for errors during safe evaluation."""
    pass

def _eval(node: ast.AST) -> float:
    """Recursively evaluate an AST node representing a mathematical expression.

    Supports binary operations (+, -, *, /), unary plus/minus, and numeric literals.
    Raises EvalError for unsupported nodes or division by zero.
    """
    if isinstance(node, ast.Expression):
        return _eval(node.body)
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            if right == 0:
                raise EvalError("Division by zero")
            return left / right
        else:
            raise EvalError(f"Unsupported binary operator: {type(node.op).__name__}")
    elif isinstance(node, ast.UnaryOp):
        operand = _eval(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        elif isinstance(node.op, ast.USub):
            return -operand
        else:
            raise EvalError(f"Unsupported unary operator: {type(node.op).__name__}")
    elif isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # For Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise EvalError("Unsupported constant type")
    else:
        raise EvalError(f"Unsupported expression: {type(node).__name__}")

def safe_eval(expr: str) -> float:
    """Parse and safely evaluate a mathematical expression string.

    Parameters
    ----------
    expr : str
        The expression to evaluate (e.g., "5*8-3").

    Returns
    -------
    float
        Result of the evaluation.

    Raises
    ------
    EvalError
        If the expression contains unsupported syntax or causes a runtime error.
    """
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise EvalError("Invalid syntax") from exc
    return _eval(parsed)

# ---------------------------------------------------------------------------
# API route
# ---------------------------------------------------------------------------
@app.route("/api/calculate", methods=["POST"])
def calculate():
    """Endpoint that accepts a JSON payload with an 'expression' key.

    Example request body: {"expression": "5*8-3"}
    Response on success: {"result": 37}
    """
    data = request.get_json(silent=True)
    if not data or "expression" not in data:
        return jsonify(error="Missing 'expression' field"), 400
    expr = data["expression"]
    if not isinstance(expr, str) or not expr.strip():
        return jsonify(error="Expression must be a non-empty string"), 400
    try:
        result = safe_eval(expr)
    except EvalError as exc:
        return jsonify(error=str(exc)), 400
    except Exception as exc:  # Catch unexpected errors (e.g., division by zero not handled above)
        return jsonify(error="Internal server error"), 500
    return jsonify(result=result), 200

# ---------------------------------------------------------------------------
# Entry point for development
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
