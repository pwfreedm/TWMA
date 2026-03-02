from flask import Flask, render_template, request, redirect, url_for
import webview

from src.core import app_core

app = Flask(__name__)

def on_close():
    app_core.shutdown()
    
def start_flask_app():
    window = webview.create_window('TWMA', app)
    window.events.closed += on_close
    webview.start()

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/form")
def form():
    return render_template("home_info.html")

@app.route("/submit", methods=["POST"])
def submit():
    app_core.enqueue(request.form.to_dict())
    return redirect(url_for('landing'))
