from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# DeclarativeBase lets you create new declarative bases in a way that's compatible w/ type checkers.
class Base(DeclarativeBase):
    pass


# Gives access to db.Model class to define models and db.session to execute queries.
db = SQLAlchemy(model_class=Base)
