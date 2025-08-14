import ast
from flask import Blueprint, request, jsonify, abort

# Define the Blueprint for calculation endpoints
calc_bp = Blueprint('calc_bp', __name__)

def _safe_eval(expr: str):
    """Evaluate a mathematical expression safely.

    Supports only basic arithmetic operators: +, -, *, / and parentheses.
    Raises ValueError if the expression contains unsupported nodes."""
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f'Invalid syntax: {e}') from None

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
                     ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.USub, ast.UAdd,
                     ast.Mod, ast.FloorDiv, ast.LParen, ast.RParen)  # LParen/RParen are not real nodes but keep for clarity

    def _check(node):
        if isinstance(node, ast.BinOp):
            if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
                raise ValueError('Unsupported operator')
            _check(node.left)
            _check(node.right)
        elif isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, (ast.UAdd, ast.USub)):
                raise ValueError('Unsupported unary operator')
            _check(node.operand)
        elif isinstance(node, (ast.Num, ast.Constant)):
            # Accept numeric constants only
            if not isinstance(getattr(node, 'n', getattr(node, 'value', None)), (int, float)):
                raise ValueError('Only numeric literals are allowed')
        elif isinstance(node, ast.Expression):
            _check(node.body)
        else:
            raise ValueError(f'Unsupported expression element: {type(node).__name__}')

    _check(node)

    # Evaluate the parsed AST safely using eval with empty globals/locals
    return eval(compile(node, '<string>', 'eval'), {}, {})

@calc_bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint to evaluate a mathematical expression sent in JSON."""
    if not request.is_json:
        return jsonify({'error': 'Request must be JSON'}), 400

    data = request.get_json()
    expr = data.get('expression')

    if not isinstance(expr, str) or not expr.strip():
        return jsonify({'error': "'expression' must be a non-empty string"}), 400

    try:
        result = _safe_eval(expr)
    except Exception as e:
        return jsonify({'error': f'Invalid expression: {str(e)}'}), 400

    return jsonify({'result': result})