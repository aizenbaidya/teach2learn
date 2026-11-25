from flask import Blueprint, render_template, jsonify, request
import anthropic

from .auth import login_required

bp = Blueprint("teach", __name__, url_prefix="/teach")
client = anthropic.Anthropic()


@bp.route("")
@login_required
def index():
    return render_template("teach/index.html")


@bp.route("/chat", methods=("POST",))
def chat():
    data = request.get_json()
    message = data.get("teacherText")
    print("\n\n\n{message}\n\n\n")

    message = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=64,
        messages=[
            {
                "role": "user",
                "content": message,
            }
        ],
    )

    output_text = [block.text for block in message.content if block.type == "text"]

    return jsonify(output_text=output_text)
