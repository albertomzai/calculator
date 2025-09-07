# backend/routes.py
from flask import Blueprint, request, jsonify
import ast
import operator as op

api_bp = Blueprint("api", __name__)

# Safe evaluation of arithmetic expressions
def safe_eval(expr):
    # Allowed operators mapping
    allowed_operators = {
        ast.Add: op.add,
        ast.Sub: op.sub,
        ast.Mult: op.mul,
        ast.Div: op.truediv,
        ast.USub: op.neg,
    }
    def _eval(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp) and type(node.op) in allowed_operators:
            left = _eval(node.left)
            right = _eval(node.right)
            return allowed_operators[type(node.op)](left, right)
        elif isinstance(node, ast.UnaryOp) and type(node.op) in allowed_operators:
            operand = _eval(node.operand)
            return allowed_operators[type(node.op)](operand)
        else:
            raise ValueError("Unsupported expression")
    node = ast.parse(expr, mode="eval").body
    return _eval(node)

@api_bp.route("/calculate", methods=["POST"])
def calculate():
    data = request.get_json()
    if not data or "expression" not in data:
        return jsonify({"error": "Missing expression"}), 400
    expr = data["expression"]
    try:
        result = safe_eval(expr)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"result": result})