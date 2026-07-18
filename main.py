import anthropic
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

load_dotenv()

client = anthropic.Anthropic()
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/welcome", response_class=HTMLResponse)
def welcome():
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Home</title>
    </head>
    <body>
        <h1>Welcome to FastAPI!</h1>
        <p>Hello World!</p>
    </body>
    </html>
    """
    return html_content


def print_message():
    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=16,
        messages=[
            {"role": "user", "content": "Hello, Claude"},
            {"role": "assistant", "content": "Hello!"},
            {"role": "user", "content": "Can you describe LLMs to me?"},
        ],
    )

    print(message)
