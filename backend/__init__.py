"""Módulo principal del backend.

Este paquete contiene la fábrica de aplicación Flask que sirve tanto el frontend (ubicado en ``frontend``) como los endpoints API.
"""

from flask import Flask

def create_app() -> Flask:
    """Crea y configura la instancia de Flask.

    Se establece la carpeta estática para servir el frontend y se registra el blueprint con las rutas de la API.
    """
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Importar y registrar los blueprints después de crear la app para evitar ciclos de importación
    from .routes import api_bp
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        """Sirve el archivo ``index.html`` del frontend."""
        return app.send_static_file('index.html')

    return app