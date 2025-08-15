"""Flask application factory for the calculator backend."""

from flask import Flask, jsonify, request
from .routes import api_bp

def create_app() -> Flask:
    """Create and configure a Flask application instance.

    The app serves static files from the frontend directory and registers
    the API blueprint that handles calculation requests.
    """
    app = Flask(__name__, static_folder="../frontend", static_url_path="")

    # Register the API Blueprint
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():  # pragma: no cover - simple static file serving
        return app.send_static_file("index.html")

    return app