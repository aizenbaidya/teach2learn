from flask import Flask, render_template
from dotenv import load_dotenv
import os

from db import db


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    db.init_app(app)

    @app.route("/")
    def homepage():
        return render_template("homepage.html")

    import auth

    app.register_blueprint(auth.bp)

    return app
