"""Backend package for the calculator application."""

from flask import Flask, send_from_directory, Blueprint, request, jsonify

# Blueprint for calculation endpoint
calc_bp = Blueprint('calc', __name__, url_prefix='/api')

def create_app():
    """Application factory that creates and configures the Flask app."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprint
    app.register_blueprint(calc_bp)

    @app.route('/')
    def index():
        """Serve the frontend entry point."""
        return send_from_directory(app.static_folder, 'index.html')

    return app