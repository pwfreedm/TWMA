from threading import Thread
import os as os
from pathlib import Path

from src.core import app_core, parse_form, app
from src.db import db
from src.forms import Consent
from src.view import init_frontend


def setup_db():
    os.makedirs(os.path.join(os.path.expanduser('~'), 'Documents', 'TWMA_DB'), exist_ok=True)
    db_path = str(Path(os.path.join(os.path.expanduser('~'), 'Documents', 'TWMA_DB')))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}/TWMA.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()


def process_form():
    while form := app_core.dequeue():
        [client, patient, appt, vet] = parse_form(form)
        Consent(client, patient, appt).generate()
        # TODO: inserting needs to change now. 
        # Database().add_record(client, patient, appt, vet)        
    
if __name__ == '__main__':
    backend = Thread(target=process_form)
    backend.start()
    setup_db()
    init_frontend()  
    backend.join()
