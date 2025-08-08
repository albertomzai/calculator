from flask import Flask, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='static')
CORS(app)

# Ruta para servir el frontend
@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

# Ruta para la API
@app.route('/api/data')
def get_data():
    # Implementa la lógica de cálculo aquí
    pass

# ...resto del código...