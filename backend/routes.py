import ast
from flask import Blueprint, request, jsonify, abort

calc_bp = Blueprint('calc', __name__)

def _safe_eval(expr: str):
    """Evaluate a mathematical expression safely.

    Only allows numbers and the operators + - * / .
    Raises ValueError if the expression is invalid."""
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f'Invalid syntax: {e}') from e

    def _validate(node):
        if isinstance(node, ast.Expression):
            return _validate(node.body)
        elif isinstance(node, ast.BinOp):
            if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
                raise ValueError('Unsupported operator')
            _validate(node.left)
            _validate(node.right)
        elif isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, (ast.UAdd, ast.USub)):
                raise ValueError('Unsupported unary operator')
            _validate(node.operand)
        elif isinstance(node, ast.Num):  # Python <3.8
            return
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if not isinstance(node.value, (int, float)):
                raise ValueError('Invalid constant type')
        else:
            raise ValueError(f'Unsupported expression: {type(node).__name__}')

    _validate(node)
    # Safe to evaluate now
    return eval(compile(node, '<string>', mode='eval'))

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint to compute a mathematical expression."""
    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()
    expr = data.get('expression')

    if not isinstance(expr, str) or not expr.strip():
        abort(400, description="'expression' must be a non-empty string")

    try:
        result = _safe_eval(expr)
    except Exception as e:
        abort(400, description=str(e))

    return jsonify({'result': result})