from flask import Blueprint, request, jsonify
import ast

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    if not data or 'expression' not in data:
        return jsonify({'error': "Missing 'expression' field"}), 400

    expression = str(data['expression']).strip()
    if len(expression) == 0:
        return jsonify({'error': "Expression cannot be empty"}), 400

    try:
        # Parse the expression safely
        node = ast.parse(expression, mode='eval')

        # Allowed nodes: Expression, BinOp, UnaryOp, Num, Constant, operators
        for subnode in ast.walk(node):
            if not isinstance(subnode, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant, ast.operator, ast.unaryop)):
                return jsonify({'error': "Invalid characters or operations"}), 400

        # Evaluate the expression safely
        result = eval(compile(node, '<string>', 'eval'), {"__builtins__": None}, {})
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': f'Error evaluating expression: {str(e)}'}), 400