from flask import Flask

def create_app():
    """Crea y configura una instancia de la aplicación Flask."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    from . import routes
    app.register_blueprint(routes.bp)

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    return app