from flask import Flask, render_template


def create_app():
    """The application factory function.

    The Flask instance is created inside this function. All configuration, registration, and setup
    that the application needs will happen in here. The application is then returned.

    Returns:
        The Flask application instance.
    """
    app = Flask(__name__, template_folder="../templates")

    @app.route("/")
    def homepage():
        return render_template("homepage.html")

    return app
