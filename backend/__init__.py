from flask import Flask, Blueprint
from backend.routes import calculate_blueprint

# Inicializar la aplicación Flask con carpetas de estáticos definidas
app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Registrar el blueprint para los endpoints de la API
app.register_blueprint(calculate_blueprint, url_prefix='/api')