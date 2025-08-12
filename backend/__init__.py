# backend package initialization

from flask import Flask

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__, static_folder='static', template_folder='templates')

    # Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')

    # Root route to serve the calculator frontend
    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app