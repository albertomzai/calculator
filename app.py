#!/usr/bin/env python3
"""
Flask application exposing a single endpoint to safely evaluate arithmetic expressions.
The logic is intentionally minimal: no database, no external services.
"""
import ast
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Allowed operators mapping for safe evaluation
ALLOWED_OPERATORS = {
    ast.Add: lambda a, b: a + b,
    ast.Sub: lambda a, b: a - b,
    ast.Mult: lambda a, b: a * b,
    ast.Div: lambda a, b: a / b,
    ast.Pow: lambda a, b: a ** b,
}


def safe_eval(node):
    """Recursively evaluate an AST node containing only allowed operators and numbers."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](left, right)
        raise ValueError("Unsupported operator")
    raise ValueError("Invalid expression component")

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json(force=True)
    if not data or 'expression' not in data:
        abort(400, description="Missing 'expression' field")
    expr_str = data['expression']
    try:
        parsed = ast.parse(expr_str, mode='eval')
        result = safe_eval(parsed.body)
    except Exception as e:
        abort(400, description=f"Invalid expression: {e}")
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
