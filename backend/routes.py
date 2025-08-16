"""

Blueprint definition for the calculator API.

Provides a single endpoint `/api/calculate` that evaluates a mathematical
expression sent in JSON format and returns the result.
"""

import re
from flask import Blueprint, request, jsonify, abort

api_bp = Blueprint('api', __name__, url_prefix='/api')

# Regular expression that only allows digits, operators, parentheses, decimal points and whitespace.
_EXPRESSION_REGEX = re.compile(r'^[0-9+\-*/().\s]+$')

def _validate_expression(expr: str) -> None:
    """Validate that the expression contains only allowed characters."""
    if not expr or not _EXPRESSION_REGEX.match(expr):
        raise ValueError('Invalid expression')

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    """Evaluate a mathematical expression sent in JSON.

    Expected payload:
        {"expression": "5*8-3"}

    Returns:
        {"result": 37} on success,
        HTTP 400 with error message on failure.
"""
    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()
    expression = data.get('expression', '')

    try:
        _validate_expression(expression)
        # Safe eval: only arithmetic operators are allowed.
        result = eval(expression, {"__builtins__": None}, {})
    except Exception as exc:
        abort(400, description=str(exc))

    return jsonify({"result": result})