from flask import Blueprint, jsonify, request
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
api = Blueprint("api", __name__, url_prefix="/api")
client = Anthropic()


@api.post("/chat")
def chat():
    data = request.get_json()
    input_text = data.get("inputText")
    message = client.messages.create(
        max_tokens=1024,
        messages=[
            {
                "content": input_text,
                "role": "user",
            }
        ],
        model="claude-opus-5-5",
    )
    output_text = [block.text for block in message.content if block.type == "text"]
    return jsonify(output_text=output_text)
