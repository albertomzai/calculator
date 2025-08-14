"""Backend package for the calculator application."""

from flask import Flask, send_from_directory

def create_app():
    """Create and configure a Flask application instance."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register the calculation blueprint
    from .routes import calc_bp
    app.register_blueprint(calc_bp)

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    return app