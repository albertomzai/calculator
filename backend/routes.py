"""Blueprint que contiene los endpoints del backend."""

import ast
from flask import Blueprint, request, jsonify


api_bp = Blueprint('api', __name__)


def _safe_eval(expr: str):
    """Evalúa una expresión aritmética de forma segura.

    Solo se permiten números y operadores + - * /. Si la expresión contiene
    cualquier otro nodo del AST, se lanza ValueError.
    """
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError('Expresión inválida') from exc

    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant,
                     ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.UAdd, ast.USub)

    for n in ast.walk(node):
        if not isinstance(n, allowed_nodes):
            raise ValueError('Operador no permitido')

    # Evaluar con un entorno vacío
    return eval(compile(node, '<string>', 'eval'), {'__builtins__': None}, {})


@api_bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint que recibe una expresión y devuelve su resultado."""
    data = request.get_json() or {}
    expression = data.get('expression')

    if not expression:
        return jsonify({'error': 'No se proporcionó la expresión'}), 400

    try:
        result = _safe_eval(expression)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 400

    return jsonify({'result': result})