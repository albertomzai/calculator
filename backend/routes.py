from flask import Blueprint, request, jsonify
import ast

calc_bp = Blueprint('calc', __name__)

# Utility to safely evaluate arithmetic expressions
def safe_eval(expr: str):
    """Evaluate a simple arithmetic expression containing only +, -, *, / operators."""
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f'Invalid syntax: {e}')

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant)
    allowed_ops = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.USub)

    for subnode in ast.walk(node):
        if not isinstance(subnode, allowed_nodes):
            raise ValueError('Disallowed expression')
        if isinstance(subnode, ast.BinOp) and not isinstance(subnode.op, allowed_ops):
            raise ValueError('Unsupported operator')
        if isinstance(subnode, ast.UnaryOp) and not isinstance(subnode.op, allowed_ops):
            raise ValueError('Unsupported unary operator')

    # Evaluate the expression safely
    return eval(compile(node, '<string>', 'eval'))

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json() or {}
    expression = data.get('expression')

    if not isinstance(expression, str) or not expression.strip():
        return jsonify({'error': 'Expression must be a non-empty string'}), 400

    try:
        result = safe_eval(expression)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'result': result})