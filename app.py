# Entry point for running the Flask application.
from backend import create_app

app = create_app()

if __name__ == '__main__':
    # Run on localhost:5000 by default
    app.run(debug=True)