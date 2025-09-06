from flask import Blueprint, request, jsonify
import math

calculate_blueprint = Blueprint('calculate', __name__)

@calculate_blueprint.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expression = data.get('expression')

    if not expression:
        return jsonify({'error': 'Falta la expresión matemática'}), 400

    try:
        result = eval(expression)
    except (SyntaxError, ZeroDivisionError) as e:
        return jsonify({'error': f'Error en la expresión: {str(e)}'}), 400

    return jsonify({'resultado': result})