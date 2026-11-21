from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    # app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_PUBLIC_URL")

    db = SQLAlchemy(app)

    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.Text, unique=True, nullable=False)
        password = db.Column(db.Text, nullable=False)

    @app.route("/")
    def homepage():
        return render_template("homepage.html")

    with app.app_context():
        db.create_all()

    # from . import auth
    import auth

    app.register_blueprint(auth.bp)

    return app
