from flask import Blueprint, request, jsonify
import ast
import operator

calculator_bp = Blueprint('calculator', __name__)

# Map of allowed operators
_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def _eval(node):
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif hasattr(ast, 'Constant') and isinstance(node, ast.Constant):  # Python >=3.8
        return node.value
    elif isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        left = _eval(node.left)
        right = _eval(node.right)
        return _OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        operand = _eval(node.operand)
        return _OPERATORS[type(node.op)](operand)
    else:
        raise ValueError("Unsupported expression")

@calculator_bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True)
    if not data or 'expression' not in data:
        return jsonify({'error': 'Missing expression'}), 400
    expr = data['expression']
    try:
        node = ast.parse(expr, mode='eval').body
        result = _eval(node)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': result})