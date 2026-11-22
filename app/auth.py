from flask import (
    Blueprint,
    render_template,
    request,
    # flash,
    redirect,
    session,
    url_for,
    g,
)
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import functools

from .db import db
from .models import User

bp = Blueprint("auth", __name__)


@bp.route("/signup", methods=("GET", "POST"))
def signup():
    if g.user:
        return redirect(url_for("homepage"))

    errors = {}

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username:
            errors["username"] = "Required!"
            return render_template("auth/signup.html", errors=errors)
        elif not password:
            errors["password"] = "Required!"
            return render_template("auth/signup.html", errors=errors)

        user = User(username=username, password=generate_password_hash(password))

        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            errors["username"] = "Invalid!"
            return render_template("auth/signup.html", errors=errors)

        return redirect(url_for("auth.login"))

    return render_template("auth/signup.html", errors=errors)


@bp.route("/login", methods=("GET", "POST"))
def login():
    if g.user:
        return redirect(url_for("homepage"))

    errors = dict()

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username:
            errors["username"] = "Required!"
        if not password:
            errors["password"] = "Required!"

        if not errors:
            user = db.session.execute(
                db.select(User).filter_by(username=username)
            ).scalar_one_or_none()

            if user is None:
                errors["username"] = "Invalid!"
            elif not check_password_hash(user.password, password):
                errors["password"] = "Invalid!"
            else:
                session.clear()
                session["user_id"] = user.id
                return redirect(url_for("homepage"))

    return render_template("auth/login.html", errors=errors)


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


@bp.before_app_request
def load_logged_in_user():
    if request.endpoint == "static":
        return

    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.get(User, user_id)


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
