import ast
from flask import Blueprint, request, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')

def _safe_eval(expr):
    """Evaluate a mathematical expression safely using AST."""
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError:
        raise ValueError('Invalid syntax')

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
                     ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd)

    for n in ast.walk(node):
        if not isinstance(n, allowed_nodes):
            raise ValueError('Disallowed expression')

    return eval(compile(node, '<string>', mode='eval'))

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    expr = data.get('expression')

    if not isinstance(expr, str) or len(expr.strip()) == 0:
        return jsonify({'error': 'Expression must be a non-empty string'}), 400

    try:
        result = _safe_eval(expr)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'result': result})