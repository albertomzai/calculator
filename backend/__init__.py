# backend package
from flask import Flask


def create_app():
    app = Flask(__name__)
    from .routes import calculator_bp
    app.register_blueprint(calculator_bp, url_prefix="/api")
    return app