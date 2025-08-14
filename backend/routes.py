"""Routes for the backend API.



This module defines a Blueprint that contains the single

``/api/calculate`` endpoint used by the frontend calculator.

"""


from flask import Blueprint, request, jsonify

# Import the specific exception class from simpleeval to handle invalid expressions.
# Using SimpleEvalError ensures we only catch errors originating from the expression evaluation
# and not other unrelated exceptions.
from simpleeval.exceptions import SimpleEvalError
from simpleeval import simple_eval


calc_bp = Blueprint("calculator", __name__, url_prefix="/api")


@calc_bp.route("/calculate", methods=["POST"])

def calculate():

    """Evaluate a mathematical expression sent by the client.



    Expects JSON payload:

        {"expression": "5*8-3"}



    Returns

    -------

    flask.Response

        JSON containing the result or an error message.

"""


    data = request.get_json(silent=True)

    if not data or "expression" not in data:

        return jsonify(error="Missing 'expression' key"), 400


    expression = data["expression"]


    try:

        result = simple_eval(expression)
        return jsonify(result=result), 200

    except SimpleEvalError as e:

        # Invalid mathematical expression supplied by the client.
        return jsonify(error=str(e)), 400

    except Exception as e:  # pragma: no cover - unexpected errors

        # Unexpected server-side error.
        return jsonify(error="Internal Server Error"), 500