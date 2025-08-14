import ast
from flask import Blueprint, request, jsonify, abort

# Blueprint for calculator API
calc_bp = Blueprint('calc', __name__, url_prefix='/api')

def _safe_eval(expr: str):
    """Evaluate a mathematical expression safely.

    Only numeric literals and the operators +, -, *, /, **, //, % are allowed.
    The function parses the expression into an AST and recursively evaluates it,
    rejecting any node that is not permitted.
    """
    try:
        tree = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f'Invalid syntax: {e}') from None

    def _eval(node):
        if isinstance(node, ast.Expression):
            return _eval(node.body)
        elif isinstance(node, ast.BinOp):
            left = _eval(node.left)
            right = _eval(node.right)
            op_type = type(node.op)

            if op_type is ast.Add:
                return left + right
            elif op_type is ast.Sub:
                return left - right
            elif op_type is ast.Mult:
                return left * right
            elif op_type is ast.Div:
                return left / right
            elif op_type is ast.Pow:
                return left ** right
            elif op_type is ast.FloorDiv:
                return left // right
            elif op_type is ast.Mod:
                return left % right
            else:
                raise ValueError('Unsupported operator')

        elif isinstance(node, ast.UnaryOp):
            operand = _eval(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            elif isinstance(node.op, ast.USub):
                return -operand
            else:
                raise ValueError('Unsupported unary operator')

        elif isinstance(node, ast.Num):  # For Python <3.8
            return node.n

        elif isinstance(node, ast.Constant):  # For Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError('Constants must be numeric')

        else:
            raise ValueError(f'Unsupported expression: {ast.dump(node)}')

    return _eval(tree)

@calc_bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint that evaluates a mathematical expression sent in JSON."""
    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()
    expression = data.get('expression', '')

    if not isinstance(expression, str) or not expression.strip():
        abort(400, description="'expression' field is required and must be a non-empty string")

    try:
        result = _safe_eval(expression)
    except Exception as e:
        abort(400, description=str(e))

    return jsonify({'result': result})