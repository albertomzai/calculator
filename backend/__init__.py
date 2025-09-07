# backend/__init__.py
from flask import Flask
from .routes import api_bp

def create_app():
    app = Flask(__name__)
    # Register API blueprint
    app.register_blueprint(api_bp, url_prefix="/api")
    return app