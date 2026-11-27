from flask import Blueprint, render_template, request

bp = Blueprint("auth", __name__)


@bp.route("/signup", methods=("GET", "POST"))
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print(username, password)
    return render_template("auth/signup.html")


@bp.route("/login")
def login():
    return render_template("auth/login.html")
