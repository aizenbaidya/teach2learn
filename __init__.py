from flask import Flask, render_template


def create_app():
    """The application factory function.

    The Flask application instance is created inside this function. All the configuration,
    registration, and setup that the application needs happens in here.

    Returns:
        The Flask application instance.
    """
    app = Flask(__name__)

    @app.route("/")
    def homepage():
        return render_template("homepage.html")

    return app
