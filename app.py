from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import ast
import operator as op

# Operadores permitidos para la evaluación segura
OPERATORS = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv,
}

app = Flask(__name__, static_folder='static')
CORS(app)  # Permite peticiones desde cualquier origen durante desarrollo

# Ruta raíz para servir la calculadora web
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Endpoint de cálculo
@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True)
    if not data or 'expression' not in data:
        return jsonify({'error': 'Missing "expression" field'}), 400
    expression = str(data['expression']).strip()
    # Validar expresión: solo dígitos, operadores + - * / y punto decimal
    allowed_chars = set('0123456789+-*/. ()')
    if any(ch not in allowed_chars for ch in expression):
        return jsonify({'error': 'Expression contains invalid characters'}), 400
    try:
        result = _safe_eval(expression)
    except ZeroDivisionError:
        return jsonify({'error': 'Division by zero'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    return jsonify({'result': result})

# Función interna para evaluar la expresión de forma segura usando ast

def _safe_eval(expr):
    node = ast.parse(expr, mode='eval')
    return _eval_node(node.body)


def _eval_node(node):
    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        operator_func = OPERATORS.get(type(node.op).__name__)
        if operator_func is None:
            raise ValueError('Unsupported operator')
        return operator_func(left, right)
    elif isinstance(node, ast.UnaryOp) and isinstance(node.op, (ast.UAdd, ast.USub)):
        operand = _eval_node(node.operand)
        return +operand if isinstance(node.op, ast.UAdd) else -operand
    elif isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError('Unsupported constant type')
    elif isinstance(node, ast.Expression):
        return _eval_node(node.body)
    else:
        raise ValueError('Invalid expression')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)