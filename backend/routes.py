"""Routes for the calculator backend.

This module defines a single Blueprint ``calc_bp`` that contains the endpoint
POST /api/calculate. The calculation logic is implemented in a helper function
`evaluate_expression` which safely evaluates mathematical expressions using only
basic arithmetic operators (+, -, *, /).  The endpoint validates input JSON and
returns either the result or an error response with status code 400.
"""

import ast
from flask import Blueprint, request, jsonify, abort

# Blueprint for calculation endpoint
calc_bp = Blueprint('calc', __name__, url_prefix='/api')


def _eval(node):
    """Recursively evaluate an AST node.

    Supports only basic arithmetic operations: +, -, *, / and numeric literals.
    Raises ValueError for any unsupported node types.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError('Unsupported constant type')

    if isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)

        if isinstance(node.op, ast.Add):
            return left + right
        elif isinstance(node.op, ast.Sub):
            return left - right
        elif isinstance(node.op, ast.Mult):
            return left * right
        elif isinstance(node.op, ast.Div):
            if right == 0:
                raise ValueError('Division by zero')
            return left / right
        else:
            raise ValueError('Unsupported binary operator')

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        return -_eval(node.operand)

    raise ValueError('Unsupported expression')


def evaluate_expression(expr: str):
    """Parse and safely evaluate a mathematical expression.

    Parameters
    ----------
    expr : str
        The arithmetic expression to evaluate.

    Returns
    -------
    float or int
        Result of the evaluation.

    Raises
    ------
    ValueError
        If the expression contains unsupported syntax or operations.
    """
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f'Invalid syntax: {e}')

    if not isinstance(parsed.body, (ast.Expression, ast.BinOp, ast.UnaryOp)) and not isinstance(parsed.body, ast.Constant):
        # Only allow a single expression
        raise ValueError('Only simple expressions are allowed')

    return _eval(parsed.body)


@calc_bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate an arithmetic expression.

    Expects JSON payload with a single key ``expression`` containing the
string representation of the mathematical expression.  Returns JSON with key ``result``.
"""

    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()

    # Validate presence and type of 'expression'
    expression = data.get('expression')
    if expression is None or not isinstance(expression, str) or not expression.strip():
        abort(400, description='"expression" must be a non-empty string')

    try:
        result = evaluate_expression(expression)
    except ValueError as e:
        abort(400, description=str(e))

    return jsonify({'result': result})