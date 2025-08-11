# backend.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import ast
import operator

app = Flask(__name__, static_folder='static')
CORS(app)

# Ruta para servir el frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Función segura de evaluación de expresiones matemáticas
allowed_operators = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}

def eval_expr(expr):
    """Evalúa una expresión aritmética simple de forma segura."""
    try:
        node = ast.parse(expr, mode='eval').body
    except SyntaxError as e:
        raise ValueError(f'Expresión inválida: {expr}') from e

    def _eval(node):
        if isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif hasattr(ast, 'Constant') and isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError('Solo se permiten números')
        elif isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = _eval(node.left)
            right = _eval(node.right)
            return allowed_operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            operand = _eval(node.operand)
            return allowed_operators[type(node.op)](operand)
        else:
            raise ValueError('Operador no permitido')

    return _eval(node)

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True)
    if not data or 'expression' not in data:
        return jsonify({'error': 'No se proporcionó la expresión'}), 400
    expr = data['expression']
    try:
        result = eval_expr(expr)
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
