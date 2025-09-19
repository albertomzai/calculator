"""Blueprint for API routes."""

from flask import Blueprint, request, jsonify
import ast

api_bp = Blueprint('api', __name__)

def _eval_expr(expr: str):
    """Safely evaluate a mathematical expression containing +,-,*,/ and parentheses."""
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError('Invalid expression') from e

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
                     ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd,
                     ast.LParen, ast.RParen) if hasattr(ast, 'LParen') else (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
                     ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd)

    for subnode in ast.walk(node):
        if not isinstance(subnode, allowed_nodes):
            raise ValueError('Disallowed expression')

    # Evaluate the parsed AST safely
    try:
        return eval(compile(node, '<string>', 'eval'), {"__builtins__": None}, {})
    except Exception as e:
        raise ValueError('Evaluation error') from e

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression sent in JSON."""
    data = request.get_json() or {}
    expr = data.get('expression')
    if not isinstance(expr, str):
        return jsonify({'error': 'Expression must be a string'}), 400

    try:
        result = _eval_expr(expr)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'result': result})