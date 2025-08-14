from flask import Flask

# Import the Blueprint from routes
from .routes import calc_bp

def create_app():
    """Create and configure a new Flask application."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register the calculation blueprint
    app.register_blueprint(calc_bp)

    return app