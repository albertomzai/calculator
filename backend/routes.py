from flask import Blueprint, request, jsonify
from simpleeval import simple_eval

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    """Evaluate a mathematical expression sent in JSON."""

    data = request.get_json(force=True)
    if not data or 'expression' not in data:
        return jsonify({'error': 'Missing "expression" key'}), 400

    expr = data['expression']

    # Validate that the expression is a string
    if not isinstance(expr, str):
        return jsonify({'error': 'Expression must be a string'}), 400

    try:
        result = simple_eval(expr)
    except Exception as e:
        # Any error during evaluation is treated as invalid expression
        return jsonify({'error': str(e)}), 400

    return jsonify({'result': result})