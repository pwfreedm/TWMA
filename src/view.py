import sys
from os import path

from flask import Flask, render_template, request, redirect, url_for
import webview

from src.core import app_core


def get_pyinstaller_path(relative_path: str) -> Path:
    """convert a traditional path into a packaged path"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = path.abspath(".")
    return path.join(base_path, relative_path)


app = Flask(
    __name__,
    template_folder=get_pyinstaller_path("templates"),
    static_folder=get_pyinstaller_path("static"),
)


def on_close():
    app_core.shutdown()


def init_frontend():
    window = webview.create_window("TWMA", app)
    window.events.closed += on_close
    webview.start(gui="qt")


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/form")
def form():
    return render_template("home_info.html")


@app.route("/submit", methods=["POST"])
def submit():
    app_core.enqueue(request.form.to_dict())
    return redirect(url_for("landing"))
