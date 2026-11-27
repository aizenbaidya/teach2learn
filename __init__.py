from flask import Flask, render_template


def create_app():
    """The application factory.

    The Flask application instance is created inside this function. All configuration, registration,
    and setup needed by the application happens in here.

    Returns:
        The Flask application instance.
    """
    app = Flask(__name__)

    @app.route("/")
    def homepage():
        return render_template("homepage.html")

    return app
