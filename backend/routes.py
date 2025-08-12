"""Blueprint que contiene las rutas de la API."""

import ast
from flask import Blueprint, request, jsonify

api_bp = Blueprint("api", __name__)

# Función auxiliar para evaluar expresiones seguras
def _safe_eval(expr: str):
    """Evalúa una expresión aritmética limitada a +,-,*,/ y números."""
    try:
        node = ast.parse(expr, mode="eval")
    except SyntaxError as e:
        raise ValueError(f"Syntax error in expression: {e}") from None

    # Recorrer el árbol y validar nodos permitidos
    for subnode in ast.walk(node):
        if isinstance(subnode, (ast.BinOp, ast.UnaryOp, ast.Num, ast.Expression, ast.Load, ast.Constant)):
            pass
        elif isinstance(subnode, ast.Name):
            raise ValueError("Variables are not allowed")
        else:
            # Operadores permitidos
            if isinstance(subnode, ast.operator) and type(subnode) in (ast.Add, ast.Sub, ast.Mult, ast.Div):
                continue
            elif isinstance(subnode, ast.unaryop) and isinstance(subnode.op, ast.UAdd | ast.USub):
                continue
            else:
                raise ValueError(f"Unsupported operation: {type(subnode).__name__}")

    # Evaluar de forma segura usando eval con dict vacío
    try:
        result = eval(compile(node, filename="<ast>", mode="eval"), {}, {})
    except Exception as e:
        raise ValueError(f"Evaluation error: {e}") from None

    return result

@api_bp.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json(silent=True)
    if not data or "expression" not in data:
        return jsonify(error="Missing 'expression' field"), 400

    expr = data["expression"]
    if not isinstance(expr, str) or len(expr.strip()) == 0:
        return jsonify(error="Expression must be a non-empty string"), 400

    try:
        result = _safe_eval(expr)
    except ValueError as e:
        return jsonify(error=str(e)), 400

    return jsonify(result=result)