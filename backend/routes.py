"""Blueprint que contiene las rutas de la API."""

from flask import Blueprint, request, jsonify
import ast

api_bp = Blueprint('api', __name__)

def _evaluate_expression(expr: str):
    """Evalúa una expresión aritmética segura usando el módulo ast."""
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError('Expresión inválida') from e

    def _visit(node):
        if isinstance(node, ast.Expression):
            return _visit(node.body)
        elif isinstance(node, ast.BinOp):
            left = _visit(node.left)
            right = _visit(node.right)
            if isinstance(node.op, ast.Add):
                return left + right
            elif isinstance(node.op, ast.Sub):
                return left - right
            elif isinstance(node.op, ast.Mult):
                return left * right
            elif isinstance(node.op, ast.Div):
                return left / right
            else:
                raise ValueError('Operador no permitido')
        elif isinstance(node, ast.Num):  # Python <3.8
            return node.n
        elif isinstance(node, ast.Constant):  # Python >=3.8
            if isinstance(node.value, (int, float)):
                return node.value
            else:
                raise ValueError('Tipo no permitido')
        else:
            raise ValueError('Nodo no permitido')

    return _visit(node)

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint que recibe una expresión y devuelve el resultado."""
    data = request.get_json(silent=True) or {}
    expr = data.get('expression')

    if not expr:
        return jsonify({'error': 'No se proporcionó expresión'}), 400

    try:
        result = _evaluate_expression(expr)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    return jsonify({'result': result})