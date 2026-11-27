from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash
from sqlalchemy.exc import IntegrityError

from db import db
from models import User

bp = Blueprint("auth", __name__)


@bp.route("/signup", methods=("GET", "POST"))
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User(username=username, password=generate_password_hash(password))
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
    return render_template("auth/signup.html")


@bp.route("/login")
def login():
    return render_template("auth/login.html")
