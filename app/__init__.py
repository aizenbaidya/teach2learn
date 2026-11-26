from flask import Flask, render_template, redirect, request
from dotenv import load_dotenv
from datetime import timedelta
import os

from .db import db
from .auth import login_required


def create_app():
    load_dotenv()

    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["TEMPLATES_AUTO_RELOAD"] = bool(os.getenv("TEMPLATES_AUTO_RELOAD"))
    app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
    db.init_app(app)

    @app.route("/")
    @login_required
    def homepage():
        return render_template("homepage.html")

    with app.app_context():
        db.create_all()
        db.engine.dispose()

    import app.auth as auth
    import app.teach as teach
    import app.reflect as reflect

    app.register_blueprint(auth.bp)
    app.register_blueprint(teach.bp)
    app.register_blueprint(reflect.bp)

    CANONICAL_HOST = os.getenv("CANONICAL_HOST")

    @app.before_request
    def redirect_to_canonical_host():
        if CANONICAL_HOST and request.host.endswith(".up.railway.app"):
            url = request.url.replace(request.host, CANONICAL_HOST, 1).replace(
                "http://", "https://", 1
            )
            return redirect(url, code=308)

    return app
