from . import create_app
from .extensions import db


def main():
    app = create_app()
    with app.app_context():
        db.create_all()  # Create the table schemas in the database (requires application context)


if __name__ == "__main__":
    main()
