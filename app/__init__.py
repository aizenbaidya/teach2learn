import os
from flask import Flask, render_template
from dotenv import load_dotenv


def create_app():
    """The application factory function.

    The Flask instance is created inside this function. All configuration, registration, and setup
    that the application needs will happen in here. The application is then returned.

    Returns:
        The Flask application instance.
    """
    load_dotenv()

    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    from .extensions import db

    db.init_app(app)

    @app.route("/")
    def homepage():
        return render_template("homepage.html")

    from . import auth

    app.register_blueprint(auth.bp)

    return app
