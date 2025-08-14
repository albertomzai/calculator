from flask import Flask, Blueprint

# Blueprint for calculation routes
calc_bp = Blueprint('calc', __name__)

def create_app() -> Flask:
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    from .routes import calc_bp as calculation_blueprint
    app.register_blueprint(calculation_blueprint)

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app

# Global app instance for testing convenience
app = create_app()