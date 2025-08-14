from flask import Blueprint, request, jsonify

from .utils import safe_eval

calc_bp = Blueprint('calc', __name__)

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression safely."""
    data = request.get_json(silent=True) or {}

    expr = data.get('expression')
    if not isinstance(expr, str) or not expr.strip():
        return jsonify({'error': 'Missing or empty "expression" field'}), 400

    try:
        result = safe_eval(expr)
    except Exception as e:
        return jsonify({'error': f'Invalid syntax: {str(e)}'}), 400

    return jsonify({'result': result})