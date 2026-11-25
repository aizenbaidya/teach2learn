from datetime import datetime, timezone
from sqlalchemy.orm import Mapped, mapped_column

from .db import db


def utcnow():
    return datetime.now(timezone.utc)


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Conversation(db.Model):
    __tablename__ = "conversations"

    id = db.Column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)
    ended_at = db.Column(db.DateTime(timezone=True))

    def __init__(self, user_id):
        self.user_id = user_id


class Message(db.Model):
    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(
        db.Integer, db.ForeignKey("conversations.id"), nullable=False, index=True
    )
    role = db.Column(db.Text, nullable=False)  # 'teacher' or 'student'
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=utcnow)

    def __init__(self, conversation_id, role, content):
        self.conversation_id = conversation_id
        self.role = role
        self.content = content
