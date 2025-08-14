from flask import Flask, send_from_directory

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register API blueprint
    from .routes import calc_bp
    app.register_blueprint(calc_bp)

    @app.route('/')
    def index():
        """Serve the frontend entry point."""
        return send_from_directory(app.static_folder, 'index.html')

    return app