"""Blueprint que contiene las rutas de la API.

Se expone un único endpoint POST ``/api/calculate`` que recibe una expresión matemática y devuelve su resultado.
"""

import ast
from flask import Blueprint, request, jsonify, abort

api_bp = Blueprint('api', __name__, url_prefix='/api')

def _safe_eval(expr: str) -> float:
    """Evalúa una expresión aritmética de forma segura.

    Se permite únicamente los operadores binarios básicos (+, -, *, /). Cualquier otro nodo del AST provoca una excepción.
    """
    try:
        node = ast.parse(expr, mode='eval')
    except SyntaxError as exc:
        raise ValueError('Expresión inválida') from exc

    class EvalVisitor(ast.NodeVisitor):
        def visit_BinOp(self, n: ast.BinOp) -> None:
            if not isinstance(n.op, (ast.Add, ast.Sub, ast.Mult, ast.Div)):
                raise ValueError('Operador no permitido')
            self.visit(n.left)
            self.visit(n.right)

        def visit_Num(self, n: ast.Num) -> None:
            pass  # Número literal aceptado

        def visit_Constant(self, n: ast.Constant) -> None:
            if not isinstance(n.value, (int, float)):
                raise ValueError('Valor no numérico')

        def generic_visit(self, node):
            # Cualquier nodo que no sea binario o número provoca error
            raise ValueError(f'Nodo no permitido: {type(node).__name__}')

    EvalVisitor().visit(node.body)

    try:
        result = eval(compile(node, '<string>', mode='eval'), {'__builtins__': None}, {})
    except Exception as exc:
        raise ValueError('Error al evaluar la expresión') from exc

    return result

@api_bp.route('/calculate', methods=['POST'])
def calculate():
    """Endpoint que recibe una expresión y devuelve su resultado."""
    data = request.get_json(silent=True)
    if not data or 'expression' not in data:
        abort(400, description='Se requiere un campo "expression" en el JSON')

    expression = str(data['expression'])

    try:
        result = _safe_eval(expression)
    except ValueError as exc:
        abort(400, description=str(exc))

    return jsonify({'result': result})