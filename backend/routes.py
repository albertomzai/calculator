"""Blueprint for calculator routes."""

from flask import Blueprint, request, jsonify
import ast

calculator_bp = Blueprint('calculator', __name__, url_prefix='/api')

# Allowed AST nodes for safe evaluation
_ALLOWED_NODES = (
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,  # For Python <3.8
    ast.Constant,  # For Python >=3.8
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub,
)

def _safe_eval(expr: str):
    """Evaluate a mathematical expression safely."""
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f'Invalid expression: {expr}') from e

    for subnode in ast.walk(node):
        if not isinstance(subnode, _ALLOWED_NODES):
            raise ValueError('Disallowed expression')

    # Compile and evaluate the node safely
    code = compile(node, '<string>', 'eval')
    return eval(code, {'__builtins__': {}})

@calculator_bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression."""
    data = request.get_json() or {}
    expr = data.get('expression', '')
    if not expr:
        return jsonify({'error': 'No expression provided'}), 400

    try:
        result = _safe_eval(expr)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'result': result})