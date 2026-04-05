from threading import Thread
import os as os

from src.core import app_core, parse_form
from src.db import *
from src.forms import FormFactory, FormType
from src.view import init_frontend


def process_form():
    while data := app_core.dequeue():
        fac = FormFactory(data)
        con = fac.generate(FormType.CONSENT)
        con.save()
        # [client, patient, appt, vet] = parse_form(form)
        # Database().add_record(client, patient, appt, vet)        
    
if __name__ == '__main__':
    backend = Thread(target=process_form)
    backend.start()
    init_frontend()  
    backend.join()
