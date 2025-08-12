from flask import Flask, jsonify

# Factory function to create and configure the Flask app
def create_app():
    """Create and return a configured Flask application instance."""

    # Configure Flask to serve static files from the frontend directory
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    from . import routes as routes_bp
    app.register_blueprint(routes_bp)

    @app.route('/')
    def index():
        """Serve the main frontend page."""
        return app.send_static_file('index.html')

    return app