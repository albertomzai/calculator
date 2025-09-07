"""Paquete backend que expone la factory create_app."""

from flask import Flask, send_from_directory
from .routes import api_bp


def create_app() -> Flask:
    """Crea y configura la aplicación Flask.

    La aplicación sirve los archivos estáticos desde el directorio ../frontend
    y registra el Blueprint de la API bajo el prefijo /api.
    """
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Ruta raíz que devuelve index.html del frontend
    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    # Registrar Blueprint de la API
    app.register_blueprint(api_bp)

    return app