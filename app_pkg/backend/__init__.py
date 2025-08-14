from flask import Flask

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    from .routes import calc_bp
    app.register_blueprint(calc_bp)

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app