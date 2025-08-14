import ast
from flask import Blueprint, request, jsonify, abort

calc_bp = Blueprint('calc', __name__)

def _safe_eval(expr: str):
    """Evaluate a mathematical expression safely.

    Supports only numbers and the operators +, -, *, /.
    Raises ValueError if the expression is invalid or contains disallowed nodes.
    """
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError('Invalid syntax') from e

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.BinOp):
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
                raise ValueError('Unsupported operator')
        elif isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
            return -_eval(node.operand)
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
            return node.value
        else:
            raise ValueError('Unsupported expression')

    return _eval(node)

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()
    expression = data.get('expression')

    if not isinstance(expression, str) or not expression.strip():
        abort(400, description="'expression' must be a non-empty string")

    try:
        result = _safe_eval(expression)
    except ValueError as e:
        abort(400, description=str(e))

    return jsonify({'result': result})