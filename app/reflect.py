from flask import Blueprint, abort, render_template, g, request

from .auth import login_required
from .models import Conversation, Message
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
    public_id = request.args.get("c")
    conversation = db.session.execute(
        db.select(Conversation).where(
            Conversation.public_id == public_id,
            Conversation.user_id == g.user.id,
        )
    ).scalar_one_or_none()
    if conversation is None:
        abort(404)
    messages = (
        db.session.execute(
            db.select(Message)
            .where(Message.conversation_id == conversation.id)
            .order_by(Message.created_at, Message.id)
        )
        .scalars()
        .all()
    )
    return render_template("reflect/view.html", messages=messages)
