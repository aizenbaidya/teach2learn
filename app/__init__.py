from flask import Flask, render_template


def create_app():
    """"""
    app = Flask(__name__, template_folder="../templates")

    @app.route("/")
    def homepage():
        return render_template("homepage.html")

    return app
