"""Package initialization for the backend.



This module creates and configures the Flask application instance.

It also registers blueprints and sets up a route to serve the

frontend index.html from the static folder.

"""


from flask import Flask, send_from_directory

import os


def create_app() -> Flask:

    """Factory function that creates and configures a Flask app.



    Returns

    -------

    flask.Flask

        The configured Flask application instance.

"""


    # The static folder is located one level above this package in the
        # ``frontend`` directory.
        app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), "..", "frontend"), static_url_path="")


    from .routes import calc_bp

    app.register_blueprint(calc_bp)


    @app.route("/")

    def serve_index():

        """Serve the main frontend page.



        Returns

        -------

        flask.Response

            The rendered index.html file.

"""

        return send_from_directory(app.static_folder, "index.html")


    return app