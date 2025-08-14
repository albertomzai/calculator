from flask import Flask, Blueprint, jsonify, request, abort

# Blueprint for calculator routes
calc_bp = Blueprint('calc', __name__)

def _safe_eval(expr):
    """Evaluate a simple mathematical expression safely."""
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expr).issubset(allowed_chars):
        raise ValueError('Expression contains invalid characters')

    try:
        # Evaluate using eval with restricted globals and locals
        result = eval(expr, {"__builtins__": None}, {})
    except Exception as e:
        raise ValueError(f'Invalid expression: {e}')
    return result

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    if not request.is_json:
        abort(400, description='Request must be JSON')

    data = request.get_json()
    expression = data.get('expression')
    if expression is None:
        abort(400, description="Missing 'expression' in request payload")

    try:
        result = _safe_eval(expression)
    except ValueError as e:
        abort(400, description=str(e))

    return jsonify({'result': result})

def create_app():
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprint
    app.register_blueprint(calc_bp)

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app