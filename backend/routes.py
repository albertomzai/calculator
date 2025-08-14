import ast
from flask import Blueprint, request, jsonify, abort

calc_bp = Blueprint('calc', __name__)

# Allowed operators for safe evaluation
_ALLOWED_OPERATORS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.USub: lambda a: -a,
}

def _evaluate(node):
    """Recursively evaluate an AST node using only allowed operators."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif hasattr(ast, 'Constant') and isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError('Unsupported constant type')
    elif isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        operand = _evaluate(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)
    else:
        raise ValueError('Unsupported expression')

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression safely."""
    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()
    expr = data.get('expression', '')

    if not isinstance(expr, str) or not expr.strip():
        abort(400, description="'expression' must be a non-empty string")

    try:
        # Parse the expression into an AST
        parsed = ast.parse(expr, mode='eval')
        result = _evaluate(parsed.body)
    except Exception as e:
        abort(400, description=f'Invalid expression: {e}')

    return jsonify({'result': result})