from flask import Blueprint, request, jsonify, abort

# Import the safe evaluation utility
from .utils import safe_eval

calc_bp = Blueprint('calc', __name__)

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression safely."""

    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()

    # Validate presence of 'expression' key and that it is a non‑empty string
    expr = data.get('expression')
    if not isinstance(expr, str) or not expr.strip():
        abort(400, description="Missing or empty 'expression' field")

    try:
        result = safe_eval(expr)
    except ValueError as e:
        # Return a 400 with the error message from safe_eval
        abort(400, description=str(e))

    return jsonify({'result': result})