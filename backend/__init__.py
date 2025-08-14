from flask import Flask, Blueprint

# Create the application factory
def create_app():
    """Create and configure a new Flask app instance."""
    # The static folder is one level up in the project root (frontend)
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    from .routes import calc_bp
    app.register_blueprint(calc_bp)

    return app