from flask import Flask, jsonify, request

# Create the application factory
def create_app():
    """Create and configure a Flask application instance."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    from .routes import calc_bp
    app.register_blueprint(calc_bp)

    # Serve the main page at root
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app