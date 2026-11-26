from flask import Blueprint, render_template, jsonify, request, g, redirect, url_for
import anthropic
from datetime import timedelta
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_neo4j import LLMGraphTransformer

from .auth import login_required
from .db import db
from .models import Conversation, Message, KnowledgeGraph
from .utils import get_file_contents, utcnow

bp = Blueprint("teach", __name__, url_prefix="/teach")
client = anthropic.Anthropic()
transformer = LLMGraphTransformer(llm=ChatOpenAI(model="gpt-6.2-astra"))

SESSION_SECONDS = 10 * 60


def extract_graph_documents(text):
    return transformer.convert_to_graph_documents([Document(page_content=text)])


def merge_elements(existing, new):
    seen = {el["data"]["id"] for el in existing}
    merged = list(existing)
    for el in new:
        if el["data"]["id"] not in seen:
            merged.append(el)
            seen.add(el["data"]["id"])
    # nodes first, so edges never point at a node that comes later in the list
    return [e for e in merged if "source" not in e["data"]] + [
        e for e in merged if "source" in e["data"]
    ]


# def create_knowledge_graph():
#     text = """
#     Marie Curie, 7 November 1867 – 4 July 1934, was a Polish and naturalized-French physicist and chemist who conducted pioneering research on radioactivity.
#     She was the first woman to win a Nobel Prize, the first person to win a Nobel Prize twice, and the only person to win a Nobel Prize in two scientific fields.
#     Her husband, Pierre Curie, was a co-winner of her first Nobel Prize, making them the first-ever married couple to win the Nobel Prize and launching the Curie family legacy of five Nobel Prizes.
#     She was, in 1906, the first woman to become a professor at the University of Paris.
#     Also, Robin Williams.
#     """
#     documents = [Document(page_content=text)]
#     llm = ChatOpenAI(model="gpt-6.2-astra")
#     transformer = LLMGraphTransformer(llm=llm)
#     graph_documents = transformer.convert_to_graph_documents(documents)
#     print(graph_documents)
#     return graph_documents


def graph_documents_to_elements(graph_documents):
    nodes = {}
    edges = []
    for doc in graph_documents:
        for node in doc.nodes:
            nodes[node.id] = {
                "data": {"id": node.id, "label": node.id, "type": node.type}
            }
        for rel in doc.relationships:
            for n in (rel.source, rel.target):
                nodes.setdefault(
                    n.id, {"data": {"id": n.id, "label": n.id, "type": n.type}}
                )
            edges.append(
                {
                    "data": {
                        "id": f"{rel.source.id}-{rel.type}-{rel.target.id}",
                        "source": rel.source.id,
                        "target": rel.target.id,
                        "label": rel.type,
                    }
                }
            )
    return list(nodes.values()) + edges


@bp.route("/knowledge-graph")
@login_required
def knowledge_graph():
    conversation = get_active_conversation(g.user.id)

    kg = db.session.execute(
        db.select(KnowledgeGraph).filter_by(conversation_id=conversation.id)
    ).scalar_one_or_none()
    if kg is None:
        kg = KnowledgeGraph(conversation_id=conversation.id)
        db.session.add(kg)

    new_messages = (
        db.session.execute(
            db.select(Message)
            .filter(
                Message.conversation_id == conversation.id,
                Message.role == "teacher",
                Message.id > kg.last_message_id,
            )
            .order_by(Message.id)
        )
        .scalars()
        .all()
    )

    if new_messages:
        text = "\n".join(m.content for m in new_messages)
        new_elements = graph_documents_to_elements(extract_graph_documents(text))
        kg.elements = merge_elements(kg.elements, new_elements)  # assign a new list
        kg.last_message_id = new_messages[-1].id

    db.session.commit()
    return jsonify(elements=kg.elements)


@bp.route("/end", methods=("POST",))
@login_required
def end():
    db.session.execute(
        db.update(Conversation)
        .where(Conversation.user_id == g.user.id, Conversation.ended_at.is_(None))
        .values(ended_at=utcnow())
    )
    db.session.commit()
    return redirect(url_for("homepage"))


@bp.route("")
@login_required
def index():
    db.session.execute(
        db.update(Conversation)
        .where(Conversation.user_id == g.user.id, Conversation.ended_at.is_(None))
        .values(ended_at=utcnow())
    )
    db.session.add(Conversation(user_id=g.user.id))
    db.session.commit()
    return render_template("teach/index.html", remaining_seconds=SESSION_SECONDS)


def get_active_conversation(user_id):
    conversation = (
        db.session.execute(
            db.select(Conversation)
            .filter_by(user_id=user_id, ended_at=None)
            .order_by(Conversation.created_at.desc())
        )
        .scalars()
        .first()
    )

    if conversation is None:
        conversation = Conversation(user_id=user_id)
        db.session.add(conversation)
        db.session.flush()

    return conversation


@bp.route("/chat", methods=("POST",))
@login_required
def chat():
    data = request.get_json()
    teacher_text = data.get("teacherText")

    conversation = get_active_conversation(g.user.id)

    elapsed_seconds = (utcnow() - conversation.created_at).total_seconds()
    if elapsed_seconds >= SESSION_SECONDS:
        conversation.ended_at = conversation.created_at + timedelta(
            seconds=SESSION_SECONDS
        )
        db.session.commit()
        return jsonify(error="Time is up!"), 403

    db.session.add(
        Message(conversation_id=conversation.id, role="teacher", content=teacher_text)
    )
    db.session.flush()

    history = (
        db.session.execute(
            db.select(Message)
            .filter_by(conversation_id=conversation.id)
            .order_by(Message.created_at, Message.id)
        )
        .scalars()
        .all()
    )

    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        output_config={"effort": "low"},
        system=get_file_contents("prompts/student-system-prompt.txt"),
        messages=[
            {
                "role": "user" if h.role == "teacher" else "assistant",
                "content": h.content,
            }
            for h in history
        ],  # type: ignore
    )

    student_text = "".join(
        block.text for block in response.content if block.type == "text"
    )

    db.session.add(
        Message(conversation_id=conversation.id, role="student", content=student_text)
    )
    db.session.commit()

    remaining_seconds = max(
        0, SESSION_SECONDS - (utcnow() - conversation.created_at).total_seconds()
    )

    return jsonify(output_text=student_text, remaining_seconds=remaining_seconds)
