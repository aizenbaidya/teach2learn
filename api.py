from flask import Blueprint, jsonify
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
api = Blueprint("api", __name__, url_prefix="/api")
client = Anthropic()


@api.post("/chat")
def chat():
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "content": "Hello!!",
                "role": "user",
            }
        ],
        model="claude-opus-5-5",
    )
    text = [block.text for block in message.content if block.type == "text"]
    return jsonify(text=text)
