from backend import create_app

app = create_app()

if __name__ == '__main__':
    # Run the development server on localhost:5000
    app.run(debug=True, host='127.0.0.1', port=5000)