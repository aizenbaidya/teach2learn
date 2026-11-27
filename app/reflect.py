from flask import Blueprint, render_template, g

from .auth import login_required
from .models import Conversation
from .db import db

bp = Blueprint("reflect", __name__, url_prefix="/reflect")


@bp.route("")
@login_required
def index():
    conversations = (
        db.session.execute(
            db.select(Conversation)
            .where(Conversation.user_id == g.user.id)
            .order_by(Conversation.created_at.desc())
        )
        .scalars()
        .all()
    )
    return render_template("reflect/index.html", conversations=conversations)


@bp.route("/view")
@login_required
def view():
    return render_template("reflect/view.html")
