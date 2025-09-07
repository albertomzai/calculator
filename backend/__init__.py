"""Backend package for the calculator application."""

from flask import Flask

def create_app() -> Flask:
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    from .routes import calculator_bp
    app.register_blueprint(calculator_bp)

    @app.route('/')
    def index():
        """Serve the frontend index.html."""
        return app.send_static_file('index.html')

    return app