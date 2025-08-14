import json
from flask import Blueprint, request, jsonify
from asteval import Interpreter

# Blueprint for the calculator API
api_bp = Blueprint('api', __name__)


def _safe_eval(expression: str) -> float:
    """Evaluate a mathematical expression safely.

    Uses ``asteval`` to parse and evaluate arithmetic expressions while
    preventing execution of arbitrary code. Only the standard Python math
    operators are allowed.
    """
    ae = Interpreter(usersyms={}, err_writer=None)
    try:
        result = ae(expression)
    except Exception as exc:
        raise ValueError(f"Invalid expression: {exc}") from None

    if ae.error:
        # ``asteval`` collects errors in the ``error`` list
        err_msg = '; '.join(str(e) for e in ae.error)
        raise ValueError(f"Expression error: {err_msg}")

    return result


@api_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint that receives a JSON payload with an ``expression`` key.

    The expression is evaluated safely and the numeric result is returned
    as JSON. If the input is missing or invalid, a 400 error is raised.
    """
    if not request.is_json:
        return jsonify({"error": "Request must be JSON."}), 400

    data = request.get_json()

    expression = data.get('expression')
    if not isinstance(expression, str):
        return jsonify({"error": "'expression' must be a string."}), 400

    try:
        result = _safe_eval(expression)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400

    return jsonify({"result": result})