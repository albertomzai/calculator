"""Blueprint that defines the calculator API."""

import re
from flask import Blueprint, request, jsonify, abort


api_bp = Blueprint("api", __name__)


_SAFE_EXPR_REGEX = re.compile(r"^[0-9+\-*/().\s]+$")


def _evaluate_expression(expr: str) -> float:
    """Safely evaluate a mathematical expression.

    The function only allows digits, decimal points and the four basic
    arithmetic operators.  It uses :func:`eval` with an empty globals
    dictionary to avoid access to built‑ins.

    Parameters
    ----------
    expr:
        String containing the mathematical expression.

    Returns
    -------
    float
        Result of evaluating ``expr``.

    Raises
    ------
    ValueError
        If the expression contains disallowed characters or if evaluation
        fails for any reason.
    """
    if not _SAFE_EXPR_REGEX.match(expr):
        raise ValueError("Expression contains unsafe characters")

    try:
        # ``eval`` is safe here because the regex guarantees only allowed chars.
        result = eval(expr, {"__builtins__": None}, {})
    except Exception as exc:
        raise ValueError(f"Failed to evaluate expression: {exc}")

    return float(result)


@api_bp.route("/calculate", methods=["POST"])
def calculate():
    """Endpoint that receives a JSON payload with an ``expression`` key.

    The expression is evaluated safely and the result returned as JSON.
    Errors in parsing or evaluation return HTTP 400.
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