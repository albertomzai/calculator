"""

Backend package for the calculator application.

This module exposes a Flask application instance via the `app` variable and
provides the factory function `create_app()` as described in the project
documentation.  The implementation is identical to the previous `app.py`
but now lives inside the official backend package.
"""

from flask import Flask

# Factory function (kept for backward compatibility)
def create_app() -> Flask:
    """Create and configure a new Flask application instance."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    from .routes import api_bp
    app.register_blueprint(api_bp)
    return app

# Expose a ready‑to‑use application instance for tests and production.
app: Flask = create_app()