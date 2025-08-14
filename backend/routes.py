"""Rutas y lógica de cálculo para el backend."""

import ast
from flask import Blueprint, request, jsonify, current_app

calc_bp = Blueprint('calc', __name__)

def _safe_eval(expr: str):
    """Evalúa de forma segura una expresión aritmética básica.

    Se permite únicamente números, operadores + - * / y paréntesis.
    """
    # Validar que la cadena contenga solo caracteres permitidos
    allowed_chars = set("0123456789+-*/(). ")
    if not set(expr).issubset(allowed_chars):
        raise ValueError('Expression contains invalid characters')

    try:
        # Parsear la expresión con ast para evitar eval inseguro
        node = ast.parse(expr, mode='eval')
        for n in ast.walk(node):
            if isinstance(n, (ast.BinOp, ast.UnaryOp, ast.Num, ast.Expression, ast.Load, ast.Expr, ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow, ast.Mod, ast.UAdd, ast.USub)):
                continue
            if isinstance(n, ast.Call):
                raise ValueError('Function calls not allowed')
            # Permitir sólo nodos aritméticos básicos
            if not isinstance(n, (ast.BinOp, ast.UnaryOp, ast.Num, ast.Expression, ast.Load, ast.Expr, ast.Constant)):
                raise ValueError('Unsupported operation in expression')
    except Exception as e:
        raise ValueError(f'Invalid expression: {e}')

    # Evaluar de forma segura con un entorno vacío
    try:
        result = eval(compile(node, '<string>', 'eval'), {'__builtins__': None}, {})
    except Exception as e:
        raise ValueError(f'Error evaluating expression: {e}')

    return result

@calc_bp.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True)
    if not data or 'expression' not in data:
        return jsonify({'error': "Missing 'expression' key"}), 400

    expr = data['expression']
    if not isinstance(expr, str) or not expr.strip():
        return jsonify({'error': 'Expression must be a non-empty string'}), 400

    try:
        result = _safe_eval(expr)
    except ValueError as e:
        current_app.logger.debug(f'Calculation error: {e}')
        return jsonify({'error': str(e)}), 400

    return jsonify({'result': result})