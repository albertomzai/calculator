# Entry point for local execution

from app_pkg import app

if __name__ == '__main__':
    # Run the Flask development server
    app.run(debug=True)