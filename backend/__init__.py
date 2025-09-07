"""Package init for backend."""

from flask import Flask

def create_app():
    """Factory que crea y configura la aplicación Flask."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Registrar blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def index():
        """Devuelve el archivo index.html del frontend."""
        return app.send_static_file('index.html')

    return app