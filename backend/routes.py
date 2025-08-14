import json
from flask import Blueprint, request, jsonify, abort
from .utils import safe_eval_expression

# Blueprint for calculator routes
calc_bp = Blueprint('calculator', __name__)

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression safely."""
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    expression = data.get('expression')

    # Validate presence and type of expression
    if expression is None or not isinstance(expression, str) or expression.strip() == '':
        return jsonify({'error': "'expression' must be a non-empty string"}), 400

    try:
        result = safe_eval_expression(expression)
    except Exception as e:
        # Return a generic error message to avoid leaking internals
        return jsonify({'error': f'Invalid expression: {str(e)}'}), 400

    return jsonify({'result': result})