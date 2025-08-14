# Root application entry point

from app_pkg.backend import create_app

app = create_app()

if __name__ == '__main__':
    # Run the development server
    app.run(debug=True)