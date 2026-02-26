from threading import Thread

from core import dequeue
from db import *
from forms import Consent
from view import start_flask_app
import os as os



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
            Client(form['client'], form['email'], form['phone'], form['address'], form['mileage']),
            Patient(form['patient'], form['animal'], form['sex'], form['weight'], form['disposal'], form['prints'], form['age'], form['breed'], form['color'], form['notes']),
            Appointment(form['date'], form['time']),
            Vet(form['vet'], form['vet_email'])
        ]
    )
    
if __name__ == '__main__':
    control = Thread(target=app_loop)
    control.start()
    start_flask_app()
    control.join()
