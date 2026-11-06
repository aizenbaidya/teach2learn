from flask import Flask, render_template

from api import api

app = Flask(__name__)
app.register_blueprint(api)


@app.route("/")
def homepage():
    return render_template("homepage.html")


@app.route("/teach")
def teach():
    return render_template("teach.html")
