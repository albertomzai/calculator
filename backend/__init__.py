from flask import Flask, jsonify, request

# Blueprint will be imported lazily to avoid circular imports
def create_app():
    """Create and configure a Flask application instance."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Register API blueprint
    from .routes import api_bp
    app.register_blueprint(api_bp)

    # Global error handlers
    @app.errorhandler(400)
    def bad_request(error):
        response = jsonify({'error': str(error.description)})
        response.status_code = 400
        return response

    @app.errorhandler(500)
    def internal_error(error):
        response = jsonify({'error': 'Internal Server Error'})
        response.status_code = 500
        return response

    return app