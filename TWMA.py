from threading import Thread
import os as os
from pathlib import Path

from src.core import app_core, parse_form, app, db
from src.db import *
from src.forms import Consent
from src.view import init_frontend


def config_app():
    db_path = str(Path(os.path.join(os.path.expanduser('~'), 'Documents', 'TWMA_DB')))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
    db.init_app(app)


def process_form():
    while form := app_core.dequeue():
        [client, patient, appt, vet] = parse_form(form)
        Consent(client, patient, appt).generate()
        Database().add_record(client, patient, appt, vet)        
    
if __name__ == '__main__':
    backend = Thread(target=process_form)
    backend.start()
    config_app()
    init_frontend()  
    backend.join()
