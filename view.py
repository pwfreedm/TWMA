from flask import Flask, render_template, request, redirect, url_for
from core import enqueue

app = Flask(__name__)

def start_flask_app(debug:bool = False):
    app.run(debug=debug)

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/form")
def form():
    return render_template("home_info.html")

@app.route("/submit", methods=["POST"])
def submit():
    enqueue(request.form.to_dict())
    return redirect(url_for('landing'))
