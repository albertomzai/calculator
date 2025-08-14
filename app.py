from app_pkg.backend import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)