from flask import Flask, render_template
from dotenv import load_dotenv
import os

from db import db
from auth import login_required


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    db.init_app(app)

    @app.route("/")
    @login_required
    def homepage():
        return render_template("homepage.html")

    import models

    with app.app_context():
        db.create_all()

    import auth

    app.register_blueprint(auth.bp)

    return app
