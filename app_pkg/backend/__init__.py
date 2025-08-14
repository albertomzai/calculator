# app_pkg.backend.__init__

# The factory creates the Flask application and exposes a global `app` for testing.

import os
from flask import Flask

def create_app():
    """Create and configure the Flask application.

    The static folder is set to the sibling ``frontend`` directory so that the
    SPA can be served directly by the backend during development.
    """
    static_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend'))

    app = Flask(__name__, static_folder=static_folder, static_url_path='')

    # Register blueprints
    from .routes import calc_bp
    app.register_blueprint(calc_bp)

    return app

# Expose a global `app` instance for tests that import from the package.
app = create_app()