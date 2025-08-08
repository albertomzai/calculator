# app/__init__.py
"""Inicializa la aplicación Flask y configura CORS."""

from flask import Flask
from flask_cors import CORS


def create_app() -> Flask:
    """Crea y devuelve una instancia de Flask configurada.

    Returns
    -------
    Flask
        La aplicación Flask con CORS habilitado y la carpeta estática establecida en ``app/static``.
    """
    app = Flask(__name__, static_folder="static")
    # Habilitamos CORS para permitir peticiones desde el frontend SPA.
    CORS(app)

    # Registramos los blueprints o rutas aquí.
    from .routes import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app
