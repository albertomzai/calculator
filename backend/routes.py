# backend/routes.py

from flask import Blueprint, request, jsonify
from .utils import safe_eval

calc_bp = Blueprint('calc', __name__)

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression."""
    data = request.get_json(silent=True) or {}

    # Validate presence of 'expression'
    if 'expression' not in data:
        return jsonify({'error': "Missing 'expression' key in JSON payload."}), 400

    expression = data['expression']

    # Validate type and non-empty string
    if not isinstance(expression, str) or not expression.strip():
        return jsonify({'error': "The 'expression' must be a non‑empty string."}), 400

    try:
        result = safe_eval(expression)
    except Exception as e:
        return jsonify({'error': f"Invalid expression: {str(e)}"}), 400

    return jsonify({'result': result})