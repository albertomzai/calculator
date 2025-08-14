import os

from flask import Flask, send_from_directory

def create_app():
    """Create and configure a Flask application instance."""

    # Determine the absolute path to the frontend directory
    frontend_path = os.path.join(os.path.dirname(__file__), '..', 'frontend')

    app = Flask(__name__, static_folder=frontend_path, static_url_path='')

    # Register blueprints and routes
    from .routes import api_bp
    app.register_blueprint(api_bp)

    @app.route('/')
    def serve_index():
        """Serve the main index.html file for the SPA."""
        return send_from_directory(app.static_folder, 'index.html')

    return app