from flask import Flask, Blueprint, jsonify, request, send_from_directory

# Blueprint for calculator routes
calc_bp = Blueprint('calc', __name__)

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register API blueprint
    from .routes import calc_bp as _calc_bp
    app.register_blueprint(_calc_bp)

    @app.route('/')
    def serve_index():
        """Serve the main index.html for the SPA."""
        return send_from_directory(app.static_folder, 'index.html')

    return app