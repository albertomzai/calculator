import ast
from flask import request, jsonify, current_app as app

# Función auxiliar para evaluar expresiones aritméticas de forma segura

def _safe_eval(expr: str):
    """Evalúa una expresión matemática básica (solo +, -, *, /) sin usar eval.
    Args:
        expr: Cadena con la expresión a evaluar.
    Returns:
        Resultado numérico de la evaluación.
    Raises:
        ValueError: Si la expresión contiene caracteres no permitidos o errores sintácticos.
    """
    # Parsear el árbol AST
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f'Syntax error in expression: {e}')

    # Recorrer nodos permitidos
    allowed_nodes = (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num,
                     ast.Constant, ast.Add, ast.Sub, ast.Mult, ast.Div,
                     ast.Pow, ast.Mod, ast.USub, ast.UAdd)

    for n in ast.walk(node):
        if not isinstance(n, allowed_nodes):
            raise ValueError(f'Unsupported expression: {expr}')

    # Evaluar usando eval con un entorno restringido
    try:
        result = eval(compile(node, '<string>', mode='eval'), {'__builtins__': None}, {})
    except Exception as e:
        raise ValueError(f'Evaluation error: {e}')

    return result

# Definir la ruta POST /api/calculate
@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json(silent=True)
    if not data or 'expression' not in data:
        return jsonify({'error': "Missing 'expression' field"}), 400
    expression = data['expression']
    if not isinstance(expression, str) or not expression.strip():
        return jsonify({'error': 'Expression must be a non-empty string'}), 400
    try:
        result = _safe_eval(expression)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    # Devolver resultado en JSON
    return jsonify({'result': result})