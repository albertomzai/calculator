from flask import Flask, send_from_directory

# Import the Blueprint from routes module
from .routes import calc_bp

def create_app():
    """Factory function to create and configure the Flask application."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register the calculation Blueprint under /api prefix
    app.register_blueprint(calc_bp, url_prefix='/api')

    @app.route('/')
    def index():
        """Serve the main frontend page."""
        return send_from_directory(app.static_folder, 'index.html')

    return app