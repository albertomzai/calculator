"""Backend package for the calculator application."""

from flask import Flask, Blueprint

__all__ = ["create_app"]

def create_app() -> Flask:
    """Create and configure a new Flask application instance.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register API blueprint
    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app