import os
from flask import Flask, render_template

from db import db


def create_app():
    """The application factory function.

    The Flask application instance is created inside this function. All the configuration,
    registration, and setup that the application needs happens in here.

    Returns:
        The Flask application instance.
    """
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")

    db.init_app(app)
    db.create_all()

    @app.route("/")
    def homepage():
        return render_template("homepage.html")

    from . import auth

    app.register_blueprint(auth.bp)

    return app
