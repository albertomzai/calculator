# Entry point for the Flask application

from backend import create_app

__name__ = "__main__"

app = create_app()

if __name__ == "__main__":
    # Run the development server
    app.run(host="0.0.0.0", port=5000, debug=True)