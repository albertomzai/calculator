from flask import Flask, Blueprint, request, jsonify, abort, current_app

# Blueprint for calculation routes
calc_bp = Blueprint('calc', __name__)

def _safe_eval(expression):
    """Evaluate a simple arithmetic expression safely."""
    allowed_chars = set("0123456789+-*/. ()")
    if not set(expression).issubset(allowed_chars):
        raise ValueError('Expression contains invalid characters')

    # Use eval with restricted globals and locals
    try:
        result = eval(expression, {"__builtins__": None}, {})
    except Exception as e:
        raise ValueError(f'Invalid expression: {e}')

    if not isinstance(result, (int, float)):
        raise ValueError('Result is not a number')
    return result

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or 'expression' not in data:
        abort(400, description="Missing 'expression' field")

    expression = data['expression']
    if not isinstance(expression, str) or not expression.strip():
        abort(400, description="Expression must be a non-empty string")

    try:
        result = _safe_eval(expression)
    except ValueError as e:
        abort(400, description=str(e))

    return jsonify({'result': result})

def create_app():
    """Application factory for the calculator backend."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    app.register_blueprint(calc_bp)

    @app.route('/')
    def index():
        return current_app.send_static_file('index.html')

    return app