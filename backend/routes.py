import ast
from flask import Blueprint, request, jsonify, abort

calc_bp = Blueprint('calc', __name__)

def _safe_eval(expr: str):
    """Evaluate a mathematical expression safely using AST."""
    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
                     ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod,
                     ast.USub, ast.UAdd, ast.FloorDiv)

    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError('Invalid syntax') from e

    for n in ast.walk(node):
        if not isinstance(n, allowed_nodes):
            raise ValueError('Disallowed expression')

    # Compile and evaluate
    code = compile(node, '<string>', 'eval')
    return eval(code, {"__builtins__": None})

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression."""
    data = request.get_json(silent=True)
    if not data or 'expression' not in data:
        return jsonify({'error': "Missing 'expression' field"}), 400

    expr = data['expression']
    if not isinstance(expr, str) or not expr.strip():
        return jsonify({'error': "Expression must be a non-empty string"}), 400

    try:
        result = _safe_eval(expr)
    except Exception as e:
        return jsonify({'error': f'Invalid expression: {str(e)}'}), 400

    return jsonify({'result': result})