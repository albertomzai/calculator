from flask import Blueprint, request, jsonify
from asteval import Interpreter

api_bp = Blueprint('api', __name__)

# Configure a safe evaluator that only allows basic arithmetic
_ae = Interpreter(usersyms={}, err_writer=None, use_numpy=False)

@api_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression sent in JSON."""
    data = request.get_json(silent=True) or {}

    if 'expression' not in data:
        return jsonify({'error': "Missing 'expression' field"}), 400

    expr = data['expression']

    if not isinstance(expr, str):
        return jsonify({'error': "Expression must be a string"}), 400

    try:
        # Use asteval to safely evaluate the expression
        result = _ae(expr)

        if _ae.error:
            raise ValueError('Invalid expression')

        return jsonify({'result': result})
    except Exception as e:
        # Return a 400 for any evaluation error
        return jsonify({'error': str(e)}), 400