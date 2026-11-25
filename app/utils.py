from datetime import datetime, timezone


def get_file_contents(filepath):
    file_contents = None

    with open(filepath) as f:
        file_contents = f.read()

    return file_contents


def utcnow():
    return datetime.now(timezone.utc)
