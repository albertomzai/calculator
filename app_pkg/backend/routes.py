# app_pkg.backend.routes

from flask import Blueprint, request, jsonify, abort
from .utils import safe_eval

# Blueprint for calculator endpoints.
calc_bp = Blueprint('calculator', __name__)

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression safely.

    Expects JSON payload: {"expression": "<math_expr>"}. Returns
    {"result": <value>} or 400 with an error message.
    """

    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()
    expression = data.get('expression')

    if not isinstance(expression, str) or not expression.strip():
        abort(400, description='"expression" must be a non‑empty string')

    try:
        result = safe_eval(expression)
    except Exception as e:
        abort(400, description=str(e))

    return jsonify({'result': result})