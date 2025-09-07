"""Flask application factory for the calculator backend."""

from flask import Flask, send_from_directory

__all__ = ["create_app"]

def create_app() -> Flask:
    """Create and configure a new Flask application instance.

    Returns:
        Flask: Configured Flask app.
    """
    app = Flask(__name__, static_folder="../frontend", static_url_path="")

    # Register blueprints
    from . import routes  # noqa: F401

    @app.route("/")
    def serve_index():
        """Serve the main frontend page."""
        return send_from_directory(app.static_folder, "index.html")

    return app