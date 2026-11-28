from flask import Blueprint, render_template, request

from .models import User
from .extensions import db

bp = Blueprint("auth", __name__)


@bp.route("/signup", methods=("GET", "POST"))
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

    return render_template("auth/signup.html")


@bp.route("/login")
def login():
    return render_template("auth/login.html")
