from flask import Blueprint, render_template

from .auth import login_required

bp = Blueprint("reflect", __name__, url_prefix="/reflect")


@bp.route("")
@login_required
def index():
    return render_template("reflect/index.html")
