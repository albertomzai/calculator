# backend/routes.py

"""Blueprint for the API routes."""

from flask import Blueprint, request, jsonify, abort
from asteval import Interpreter

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """Evaluate a mathematical expression sent in JSON.

    Expects: {"expression": "5*8-3"}
    Returns: {"result": 37} or a 400 error with message.
    """
    data = request.get_json(force=True, silent=False)
    if not data or 'expression' not in data:
        abort(400, description='Missing "expression" field')

    expression = data['expression']
    if not isinstance(expression, str):
        abort(400, description='Expression must be a string')

    # Safe evaluation using asteval
    interpreter = Interpreter(usersyms={}, err_writer=None)
    try:
        result = interpreter(expression)
    except Exception as e:
        abort(400, description=f'Invalid expression: {e}')

    if interpreter.error:
        # Collect all error messages from asteval
        errors = '; '.join([str(err.get_error()) for err in interpreter.error])
        abort(400, description=f'Evaluation error: {errors}')

    return jsonify({'result': result})