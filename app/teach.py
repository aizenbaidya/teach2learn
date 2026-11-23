from flask import Blueprint, render_template

from .auth import login_required

bp = Blueprint("teach", __name__, url_prefix="/teach")


@bp.route("")
@login_required
def index():
    return render_template("teach/index.html")
