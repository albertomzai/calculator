from flask import Flask, Blueprint, request, jsonify

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='')

    # Register blueprints
    from .routes import api_bp
    app.register_blueprint(api_bp)

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app