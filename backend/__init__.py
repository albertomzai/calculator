from flask import Flask, send_from_directory

def create_app():
    """Factory function to create and configure the Flask app."""
    # The static folder is one level up in 'frontend'.
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register blueprints
    from .routes import calc_bp
    app.register_blueprint(calc_bp)

    @app.route('/')
    def serve_root():
        """Serve the main index.html file for the frontend."""
        return send_from_directory(app.static_folder, 'index.html')

    return app