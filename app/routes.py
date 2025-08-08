# app/routes.py
"""Define las rutas de la API."""

from flask import Blueprint, request, jsonify, abort
import ast
import operator as op

bp = Blueprint("api", __name__)

# Mapa seguro de operadores permitidos.
OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _eval(node):
    """Evalúa de forma segura un árbol AST que representa una expresión aritmética.

    Parameters
    ----------
    node : ast.AST
        Nodo del árbol a evaluar.

    Returns
    -------
    float | int
        Resultado numérico de la evaluación.
    """
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Solo se permiten números")
    elif isinstance(node, ast.BinOp) and type(node.op) in OPERATORS:
        left = _eval(node.left)
        right = _eval(node.right)
        try:
            result = OPERATORS[type(node.op)](left, right)
        except ZeroDivisionError as e:
            raise ZeroDivisionError("División por cero") from e
        return result
    elif isinstance(node, ast.UnaryOp) and type(node.op) in OPERATORS:
        operand = _eval(node.operand)
        return OPERATORS[type(node.op)](operand)
    else:
        raise ValueError(f"Operador no permitido: {ast.dump(node)}")


@bp.route("/calculate", methods=["POST"])
def calculate():
    """Evalúa una expresión matemática enviada en el cuerpo JSON.

    El cuerpo debe ser un objeto JSON con la clave ``expression`` que contenga una cadena.
    Si la evaluación es exitosa, devuelve ``{"result": valor}``.
    En caso de error (JSON inválido, falta la clave, sintaxis incorrecta o división por cero)
    responde con status 400 y un mensaje descriptivo.
    """
    if not request.is_json:
        abort(400, description="El cuerpo debe ser JSON")

    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "expression" not in data:
        abort(400, description="Se requiere la clave 'expression' con una cadena válida")

    expression = data["expression"]
    if not isinstance(expression, str):
        abort(400, description="La expresión debe ser una cadena")

    try:
        tree = ast.parse(expression, mode="eval")
        result = _eval(tree.body)
    except ZeroDivisionError as e:
        abort(400, description=str(e))
    except Exception as e:
        # Cualquier otro error (sintaxis, operadores no permitidos, etc.)
        abort(400, description=f"Expresión inválida: {e}")

    return jsonify({"result": result})
