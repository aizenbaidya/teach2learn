from flask import Blueprint, render_template, jsonify, request, g, redirect, url_for
import anthropic
from datetime import timedelta

from .auth import login_required
from .db import db
from .models import Conversation, Message
from .utils import get_file_contents, utcnow

bp = Blueprint("teach", __name__, url_prefix="/teach")
client = anthropic.Anthropic()

SESSION_SECONDS = 10 * 60


@bp.route("/end", methods=("POST",))
@login_required
def end():
    db.session.execute(
        db.update(Conversation)
        .where(Conversation.user_id == g.user.id, Conversation.ended_at.is_(None))
        .values(ended_at=utcnow())
    )
    db.session.commit()
    return redirect(url_for("homepage"))


@bp.route("")
@login_required
def index():
    db.session.execute(
        db.update(Conversation)
        .where(Conversation.user_id == g.user.id, Conversation.ended_at.is_(None))
        .values(ended_at=utcnow())
    )
    db.session.add(Conversation(user_id=g.user.id))
    db.session.commit()
    return render_template("teach/index.html", remaining_seconds=SESSION_SECONDS)


def get_active_conversation(user_id):
    conversation = (
        db.session.execute(
            db.select(Conversation)
            .filter_by(user_id=user_id, ended_at=None)
            .order_by(Conversation.created_at.desc())
        )
        .scalars()
        .first()
    )

    if conversation is None:
        conversation = Conversation(user_id=user_id)
        db.session.add(conversation)
        db.session.flush()

    return conversation


@bp.route("/chat", methods=("POST",))
@login_required
def chat():
    data = request.get_json()
    teacher_text = data.get("teacherText")

    conversation = get_active_conversation(g.user.id)

    elapsed_seconds = (utcnow() - conversation.created_at).total_seconds()
    if elapsed_seconds >= SESSION_SECONDS:
        conversation.ended_at = conversation.created_at + timedelta(
            seconds=SESSION_SECONDS
        )
        db.session.commit()
        return jsonify(error="Time is up!"), 403

    db.session.add(
        Message(conversation_id=conversation.id, role="teacher", content=teacher_text)
    )
    db.session.flush()

    history = (
        db.session.execute(
            db.select(Message)
            .filter_by(conversation_id=conversation.id)
            .order_by(Message.created_at, Message.id)
        )
        .scalars()
        .all()
    )

    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        output_config={"effort": "low"},
        system=get_file_contents("prompts/student-system-prompt.txt"),
        messages=[
            {
                "role": "user" if h.role == "teacher" else "assistant",
                "content": h.content,
            }
            for h in history
        ],  # type: ignore
    )

    student_text = "".join(
        block.text for block in response.content if block.type == "text"
    )

    db.session.add(
        Message(conversation_id=conversation.id, role="student", content=student_text)
    )
    db.session.commit()

    remaining_seconds = max(
        0, SESSION_SECONDS - (utcnow() - conversation.created_at).total_seconds()
    )

    return jsonify(output_text=student_text, remaining_seconds=remaining_seconds)
