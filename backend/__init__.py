from flask import Flask, send_from_directory

def create_app():
    """Factory function that creates and configures the Flask app."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register the calculator blueprint
    from .routes import calc_bp as _calc_bp
    app.register_blueprint(_calc_bp)

    @app.route('/')
    def serve_index():
        """Serve the frontend index.html file."""
        return send_from_directory(app.static_folder, 'index.html')

    return app