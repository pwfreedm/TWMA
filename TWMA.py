from threading import Thread
import os as os

from src.core import app_core, app
from src.db import *
from src.forms import FormFactory, FormType
from src.view import init_frontend
from src.update import downlaod_update, needs_update


def setup_app():
    os.makedirs(app_core.settings.db_path, exist_ok=True)
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{app_core.settings.db_path}/TWMA.db"
    app.config['SECRET_KEY'] = app_core.settings.get_secret_key()
    db.init_app(app)
    app_core.setup_fps()
    with app.app_context():
        db.create_all()

def process_form():
    while data := app_core.dequeue():
        if (data['form_id'] == 'settings'):
            print(data)
            res = app_core.settings.update_settings(data)
        elif (data['form_id'] == 'vet_info'):
            register_vet(data)
        else:
            fac = FormFactory(data)
            con = fac.generate(FormType.CONSENT)
            con.save()
            bom = fac.generate(FormType.BILL_OF_MATERIALS)
            bom.save()
            register_pt(data)

if __name__ == '__main__':
    try:
        setup_app()
        backend = Thread(target=process_form)
        update = Thread(target=downlaod_update)

        backend.start()
        has_update = needs_update()
        if (has_update):
            update.start()

        init_frontend(update=has_update)

        update.join()
        backend.join()
    except Exception as e:
        quit()
