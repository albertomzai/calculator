# backend/__init__.py

from flask import Flask

def create_app() -> Flask:
    """Factory function that creates and configures the Flask application."""
    app = Flask(__name__, static_folder="../frontend", static_url_path="")

    # Register API routes
    from .routes import api_bp
    app.register_blueprint(api_bp)

    return app