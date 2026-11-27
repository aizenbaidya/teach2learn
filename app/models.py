from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import db


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(Text, unique=True)
    password: Mapped[str] = mapped_column(Text)

    def __init__(self, username, password):
        self.username = username
        self.password = password
