from flask import Flask, request, jsonify
from flask_cors import CORS
import ast

app = Flask(__name__, static_folder='static')
CORS(app)

# Ruta raíz para servir el frontend
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Validación segura de la expresión
ALLOWED_NODES = {
    ast.Expression,
    ast.BinOp,
    ast.UnaryOp,
    ast.Num,
    ast.Constant,
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
    ast.USub
}

def safe_eval(expr: str):
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError('Invalid expression syntax') from e
    for node in ast.walk(parsed):
        if type(node) not in ALLOWED_NODES:
            raise ValueError(f'Unsupported operation: {type(node).__name__}')
    try:
        result = eval(compile(parsed, '<string>', mode='eval'), {}, {})
    except ZeroDivisionError as e:
        raise ValueError('Division by zero') from e
    return result

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json(force=True)
    if not data or 'expression' not in data:
        return jsonify({'error': 'Missing expression'}), 400
    expr = data['expression']
    try:
        result = safe_eval(expr)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': result})
