from flask import Blueprint, request, jsonify
from .utils import safe_eval

calc_bp = Blueprint('calc', __name__)

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    expression = data.get('expression')

    if not isinstance(expression, str) or not expression.strip():
        return jsonify({'error': 'Expression must be a non-empty string'}), 400

    try:
        result = safe_eval(expression)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'result': result})