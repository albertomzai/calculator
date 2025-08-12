from flask import Blueprint, request, jsonify
import ast

# Blueprint for API routes
bp = Blueprint('api', __name__, url_prefix='/api')

# Allowed operators mapping for safe evaluation
_allowed_ops = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b
}  # type: ignore

def _eval_node(node):
    """Recursively evaluate an AST node safely."""
    if isinstance(node, ast.Num):  # For Python <3.8
        return node.n
    if hasattr(ast, 'Constant') and isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _allowed_ops:
            raise ValueError(f"Operator {op_type} is not allowed")
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _allowed_ops[op_type](left, right)

    if isinstance(node, ast.UnaryOp) and isinstance(node.op, ast.USub):
        operand = _eval_node(node.operand)
        return -operand

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def evaluate_expression(expr: str):
    """Evaluate a mathematical expression string safely."""
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError("Invalid syntax") from e

    if not isinstance(parsed.body, (ast.BinOp, ast.UnaryOp, ast.Num)) and not hasattr(ast, 'Constant'):
        raise ValueError("Unsupported expression type")

    return _eval_node(parsed.body)

@bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression sent in JSON."""
    data = request.get_json(force=True, silent=True)
    if not data or 'expression' not in data:
        return jsonify({'error': 'Missing "expression" field'}), 400

    expr = data['expression']
    if not isinstance(expr, str):
        return jsonify({'error': 'The "expression" must be a string'}), 400

    try:
        result = evaluate_expression(expr)
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero is not allowed'}), 422
    except ValueError as e:
        return jsonify({'error': str(e)}), 422

    return jsonify({'result': result}), 200