"""Backend package initialization."""

from flask import Flask
from .routes import api_bp


def create_app() -> Flask:
    """Factory function that creates and configures the Flask app.

    The application serves static files from the ``../frontend`` directory
    and registers the API blueprint defined in :mod:`backend.routes`.

    Returns
    -------
    flask.Flask
        Configured Flask application instance.
    """
    app = Flask(__name__, static_folder="../frontend", static_url_path="")

    # Register API blueprint
    app.register_blueprint(api_bp, url_prefix="/api")

    return app