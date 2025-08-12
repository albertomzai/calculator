from flask import Blueprint, request, jsonify
import ast

api_bp = Blueprint('api', __name__)

# Supported operators for safe evaluation
_OPERATORS = {ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd}

def _eval_node(node):
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    elif isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    elif hasattr(ast, 'Constant') and isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError('Unsupported constant type')
    elif isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Add): return left + right
        if isinstance(node.op, ast.Sub): return left - right
        if isinstance(node.op, ast.Mult): return left * right
        if isinstance(node.op, ast.Div): return left / right
        if isinstance(node.op, ast.Pow): return left ** right
    elif isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        operand = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd): return +operand
        if isinstance(node.op, ast.USub): return -operand
    raise ValueError('Unsupported expression')

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True)
    if not data or 'expression' not in data:
        return jsonify({'error': "Missing 'expression' key"}), 400

    expr = str(data['expression']).strip()
    if len(expr) == 0:
        return jsonify({'error': 'Expression cannot be empty'}), 400

    try:
        parsed = ast.parse(expr, mode='eval')
        result = _eval_node(parsed)
    except Exception as e:
        return jsonify({'error': f'Invalid expression: {str(e)}'}), 400

    return jsonify({'result': result})