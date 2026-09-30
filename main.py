import random
from string import hexdigits
import anthropic
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

load_dotenv()

client = anthropic.Anthropic()
app = FastAPI()

# app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="dist/assets"), name="assets")
templates = Jinja2Templates(directory="templates")


@app.get("/hello-world")
def read_root():
    return {"Hello": "World"}


@app.get("/random-color", response_class=HTMLResponse)
def random_color(request: Request):
    hex_chars = "".join(random.choices(hexdigits.lower(), k=6))
    hex_color = f"#{hex_chars}"
    context = {"color": hex_color}
    return templates.TemplateResponse(
        request=request, name="color.html", context=context
    )


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


app.mount("/", StaticFiles(directory="dist", html=True), name="dist")
