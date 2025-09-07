"""Flask application factory for the calculator backend."""

from flask import Flask, send_from_directory

__all__ = ["create_app", "app"]

def create_app():
    """Create and configure a new Flask application instance.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    from . import routes
    app.register_blueprint(routes.bp)

    @app.route('/')
    def serve_index():
        """Serve the main frontend page.

        Returns:
            Response: The index.html file served as static content.
        """
        return send_from_directory(app.static_folder, 'index.html')

    return app

# Create a global app instance for testing and running directly.
app = create_app()