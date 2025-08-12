import ast
from flask import Blueprint, request, jsonify, abort

api_bp = Blueprint('api', __name__)

# Allowed operators for safe evaluation
_ALLOWED_OPERATORS = {ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub}

def _eval_expr(node):
    """Recursively evaluate an AST node representing a mathematical expression."""
    if isinstance(node, ast.Num):  # <Python 3.8
        return node.n
    elif hasattr(ast, 'Constant') and isinstance(node, ast.Constant):  # Python 3.8+
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError('Unsupported constant type')
    elif isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _eval_expr(node.left)
        right = _eval_expr(node.right)
        if isinstance(node.op, ast.Add): return left + right
        if isinstance(node.op, ast.Sub): return left - right
        if isinstance(node.op, ast.Mult): return left * right
        if isinstance(node.op, ast.Div):
            if right == 0:
                raise ZeroDivisionError('division by zero')
            return left / right
        if isinstance(node.op, ast.Pow): return left ** right
    elif isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        operand = _eval_expr(node.operand)
        if isinstance(node.op, ast.USub): return -operand
    raise ValueError('Unsupported expression')

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True) or {}
    expr = data.get('expression')

    if not isinstance(expr, str):
        return jsonify({'error': "'expression' must be a string"}), 400

    try:
        parsed = ast.parse(expr, mode='eval').body
        result = _eval_expr(parsed)
    except ZeroDivisionError as e:
        return jsonify({'error': str(e)}), 422
    except Exception as e:
        return jsonify({'error': 'Invalid expression'}), 422

    return jsonify({'result': result})