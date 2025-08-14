"""Routes for the calculator backend."""

import ast
from flask import request, jsonify, current_app
from . import calc_bp

# Allowed operators mapping for safe evaluation
_OPERATORS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
}

def _eval(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Num):  # <number> (Python <3.8)
        return node.n
    elif hasattr(ast, 'Constant') and isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    elif isinstance(node, ast.BinOp):
        left = _eval(node.left)
        right = _eval(node.right)
        op_type = type(node.op)
        if op_type in _OPERATORS:
            try:
                return _OPERATORS[op_type](left, right)
            except ZeroDivisionError:
                raise ValueError('division by zero')
        else:
            raise ValueError(f'Unsupported operator: {op_type}')
    else:
        raise ValueError(f'Unsupported expression component: {type(node)}')

@calc_bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint that evaluates a mathematical expression sent in JSON."""
    if not request.is_json:
        return jsonify(error='Request must be JSON'), 400

    data = request.get_json()

    # Validate presence and type of 'expression'
    expr = data.get('expression')
    if expr is None or not isinstance(expr, str) or expr.strip() == '':
        return jsonify(error="'expression' must be a non-empty string"), 400

    try:
        # Parse expression into AST
        tree = ast.parse(expr, mode='eval')
        result = _eval(tree.body)
    except Exception as e:
        current_app.logger.debug(f'Expression evaluation error: {e}')
        return jsonify(error=f'Invalid expression: {str(e)}'), 400

    return jsonify(result=result)