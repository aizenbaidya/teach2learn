import anthropic
from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

client = anthropic.Anthropic()
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


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
