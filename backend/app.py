"""Entry point for running the Flask application."""

from . import create_app, app

if __name__ == "__main__":
    # Run the development server
    app.run(host='0.0.0.0', port=5000, debug=True)