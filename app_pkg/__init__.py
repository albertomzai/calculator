# Expose the Flask application instance for tests and other imports

from backend import create_app

app = create_app()