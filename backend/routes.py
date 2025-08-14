from flask import Blueprint, request, jsonify
from simpleeval import simple_eval, SimpleEvalError

api_bp = Blueprint('api', __name__)

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    """Evaluate a mathematical expression safely and return the result."""
    data = request.get_json(silent=True) or {}
    expression = data.get('expression')

    if not isinstance(expression, str):
        return jsonify({'error': 'Expression must be a string.'}), 400

    try:
        result = simple_eval(expression)
    except SimpleEvalError as exc:
        return jsonify({'error': f'Invalid expression: {exc}'}), 400
    except Exception as exc:
        # Catch any unforeseen errors during evaluation
        return jsonify({'error': f'Evaluation error: {exc}'}), 500

    return jsonify({'result': result})