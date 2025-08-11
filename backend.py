from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import ast
import operator as op

app = Flask(__name__, static_folder='static')
CORS(app)

# Ruta raíz para servir el frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Función segura para evaluar expresiones aritméticas simples
_ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

def _eval(node):
    if isinstance(node, ast.Num):  # <Python 3.8
        return node.n
    elif hasattr(ast, 'Constant') and isinstance(node, ast.Constant):  # Python 3.8+
        return node.value
    elif isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPERATORS:
        left = _eval(node.left)
        right = _eval(node.right)
        return _ALLOWED_OPERATORS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPERATORS:
        operand = _eval(node.operand)
        return _ALLOWED_OPERATORS[type(node.op)](operand)
    else:
        raise ValueError('Unsupported expression')

# API para calcular expresiones
@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True)
    if not data or 'expression' not in data:
        return jsonify({'error': 'Missing "expression" field'}), 400
    expr = str(data['expression']).strip()
    try:
        node = ast.parse(expr, mode='eval').body
        result = _eval(node)
    except Exception as e:
        return jsonify({'error': f'Invalid expression: {str(e)}'}), 400
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)