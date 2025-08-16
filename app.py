# app.py

from backend import create_app

# Expose the Flask application instance at module load time
app = create_app()

if __name__ == "__main__":
    # Run the development server when executed directly
    app.run(host="0.0.0.0", port=5000, debug=True)