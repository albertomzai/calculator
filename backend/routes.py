from flask import Blueprint, request, jsonify
bp = Blueprint('calc', __name__)
@bp.route('/api/calculate', methods=['POST'])
def calculate():
    expression = request.json.get('expression')
    try:
        result = eval(expression)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 400