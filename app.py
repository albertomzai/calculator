from backend import create_app

# Create the Flask instance that will be used by tests and external clients.
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)