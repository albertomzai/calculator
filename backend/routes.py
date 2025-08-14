from flask import request, jsonify, current_app
from .utils import safe_eval

@current_app.calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True)
    if not data or 'expression' not in data:
        return jsonify({'error': "Missing 'expression' key"}), 400

    expression = data['expression']
    if not isinstance(expression, str) or not expression.strip():
        return jsonify({'error': "Expression must be a non-empty string"}), 400

    try:
        result = safe_eval(expression)
    except Exception as e:
        return jsonify({'error': f'Invalid expression: {str(e)}'}), 400

    return jsonify({'result': result})