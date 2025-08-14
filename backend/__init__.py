from flask import Flask, send_from_directory

# Blueprint for API routes
from .routes import api_bp

__all__ = ['create_app']


def create_app():
    """Factory function that creates and configures the Flask app.

    The application serves static files from the ``frontend`` directory
    (the index.html of the calculator) and registers the API blueprint.
    """
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register the API blueprint
    app.register_blueprint(api_bp)

    @app.route('/')
    def serve_index():
        """Serve the calculator frontend."""
        return send_from_directory(app.static_folder, 'index.html')

    # Global error handler for unhandled exceptions in the API
    @app.errorhandler(Exception)
    def handle_exception(e):
        """Return JSON error responses for unexpected server errors."""
        response = {"error": str(e)}
        return response, 500

    return app