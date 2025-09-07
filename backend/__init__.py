"""Backend package for the calculator API."""

from flask import Flask, jsonify, request
import ast

__all__ = ["create_app"]

def create_app():
    """Factory function that creates and configures the Flask app.

    Returns:
        Flask: Configured Flask application instance.
    """
    app = Flask(__name__, static_folder="../frontend", static_url_path="")

    # Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.route("/")
    def index():
        """Serve the frontend entry point."""
        return app.send_static_file("index.html")

    return app