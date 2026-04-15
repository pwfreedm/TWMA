from threading import Thread
import os as os
from pathlib import Path

from src.core import app_core, app
from src.db import *
from src.forms import FormFactory, FormType
from src.view import init_frontend
from src.utils import wrap_path


def setup_db():
    os.makedirs(os.path.join(os.path.expanduser('~'), 'Documents', 'TWMA_DB'), exist_ok=True)
    db_path = str(Path(os.path.join(os.path.expanduser('~'), 'Documents', 'TWMA_DB')))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}/TWMA.db"
    db.init_app(app)
    with app.app_context():
        db.create_all()


def process_form():
    while data := app_core.dequeue():
        fac = FormFactory(data)
        con = fac.generate(FormType.CONSENT)
        con.save()
        bom = fac.generate(FormType.BILL_OF_MATERIALS)
        bom.save()
        register_pt(data)
    
if __name__ == '__main__':
    backend = Thread(target=process_form)
    backend.start()
    setup_db()
    init_frontend()  
    backend.join()
