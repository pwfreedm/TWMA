from threading import Thread
import os as os

from src.core import dequeue, address
from src.db import *
from src.forms import Consent
from src.view import start_flask_app


def app_loop():
    should_quit = False
    while not should_quit:
        form = dequeue()
        [client, patient, appt, vet] = parse_form(form)
        Consent(client, patient, appt).generate()
        Database().add_record(client, patient, appt, vet)        

def parse_form(form: dict[str, str]) -> tuple[Client, Patient, Appointment, Vet]:
    return tuple(
        [
            Client(form['client'], form['email'], form['phone'], address(form['address'], form['city'], form['state'], form['zip'])),
            Patient(form['patient'], form['animal'], form['sex'], form['weight'], form['disposal'], form['prints'], form['age'], form['breed'], form['color'], form['notes']),
            Appointment(form['date'], form['time']),
            Vet(form['vet'])
        ]
    )
    
if __name__ == '__main__':
    control = Thread(target=app_loop)
    control.start()
    start_flask_app()
    control.join()
