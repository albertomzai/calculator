import ast

from flask import Blueprint, request, jsonify, abort

# Blueprint for calculator endpoints
calc_bp = Blueprint('calc', __name__)

def _safe_eval(expr: str) -> float:
    """Evaluate a mathematical expression safely.

    Supports only +, -, *, / and parentheses."""
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError:
        raise ValueError('Invalid syntax')

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp,
                     ast.Num, ast.Constant, ast.Add, ast.Sub,
                     ast.Mult, ast.Div, ast.Pow, ast.USub,
                     ast.UAdd, ast.Load, ast.Tuple, ast.List,
                     ast.Name, ast.Call)

    for n in ast.walk(node):
        if not isinstance(n, allowed_nodes):
            raise ValueError('Disallowed expression')

    # Only allow numeric constants and arithmetic ops
    try:
        result = eval(compile(node, '<string>', 'eval'), {"__builtins__": None}, {})
    except Exception as e:
        raise ValueError('Evaluation error') from e

    return result

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()
    expression = data.get('expression')

    if not isinstance(expression, str) or not expression.strip():
        abort(400, description="'expression' must be a non‑empty string")

    try:
        result = _safe_eval(expression)
    except ValueError as e:
        abort(400, description=str(e))

    return jsonify({'result': result})

def create_app():
    from flask import Flask

    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    app.register_blueprint(calc_bp)

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app