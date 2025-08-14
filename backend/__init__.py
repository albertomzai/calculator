# backend/__init__.py

from flask import Flask
from .routes import calc_bp

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    app.register_blueprint(calc_bp)

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app

# Expose the app instance for tests and other imports
app = create_app()