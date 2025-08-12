"""Package inicializador para la aplicación backend."""

from flask import Flask, Blueprint

# Importar blueprint de rutas
from .routes import api_bp

def create_app() -> Flask:
    """Factory function que crea y configura la app Flask."""
    app = Flask(__name__, static_folder="../frontend", static_url_path="")

# Registrar blueprint de API
    app.register_blueprint(api_bp, url_prefix="/api")

# Ruta raíz para servir index.html del frontend
    @app.route("/")
    def root():
        return app.send_static_file("index.html")

    return app