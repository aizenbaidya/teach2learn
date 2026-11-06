from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/teach")
def teach():
    return render_template("teach.html")
