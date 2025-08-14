# backend/__init__.py

"""Package initialization for the backend module."""

from flask import Flask, send_from_directory, jsonify, abort
from .routes import api_bp

__all__ = ['create_app']

def create_app():
    """Factory that returns a Flask application.

    The function is defined in the original code, but we keep a lightweight
    wrapper here to guarantee its presence when the package is imported.
    """
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register API blueprint
    app.register_blueprint(api_bp)

    @app.route('/')
    def serve_index():
        return send_from_directory(app.static_folder, 'index.html')

    @app.errorhandler(Exception)
    def handle_exception(e):
        # If the exception has a code attribute (e.g., abort(400)), use it
        code = getattr(e, 'code', 500)
        message = str(e) if isinstance(e, Exception) else e.description
        return jsonify({'error': message}), code

    return app