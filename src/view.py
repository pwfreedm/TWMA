from flask import render_template, request, redirect, url_for
import webview

from src.db import Client, Vet, Patient, Appointment, db
from src.core import app, app_core
from src.update import install_patch

def on_close():
    app_core.shutdown()

def init_frontend(update: bool):
    window = webview.create_window("TWMA", app)
    window.events.closed += on_close
    if update:
        window.events.closed += install_patch
    webview.start(gui="qt")

@app.route("/")
def landing():
    return render_template("landing.html")

@app.route("/new_patient")
def new_patient():
    vets = Vet.query.all()
    return render_template("home_info.html", vets=vets)

@app.route("/new_vet")
def new_vet():
    return render_template("vet_info.html")

@app.route("/lookup", methods=["POST", "GET"])
def lookup_record():
    matches= None
    if request.method == 'POST':
        s = db.session
        name = request.form.get('client').lower()
        match = s.query(Client).join(Patient.owner).join(Patient.appt).where(Client.name == name).one_or_none()
        return render_template("lookup.html", match=match)
        
    return render_template("lookup.html", matches=None)

@app.route("/settings")
def settings(db_path: str = app_core.settings.db_path, out_path: str = app_core.settings.out_path):
    return render_template("settings.html", 
                           db_path=db_path, 
                           out_path=out_path
                           )

@app.route("/submit", methods=["POST"])
def submit():
    app_core.enqueue(request.form.to_dict())
    return redirect(url_for("landing"))

@app.route("/update", methods=["POST"])
def update():
    app_core.enqueue(request.form.to_dict())
    return settings(db_path=request.form.get('db_path'), out_path=request.form.get('out_path'))
