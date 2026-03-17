from threading import Thread
import os as os

from src.core import app_core, parse_form
from src.db import *
from src.forms import Consent
from src.view import init_frontend


def process_form():
    while form := app_core.dequeue():
        [client, patient, appt, vet] = parse_form(form)
        Consent(client, patient, appt).generate()
        Database().add_record(client, patient, appt, vet)        
    
if __name__ == '__main__':
    backend = Thread(target=process_form)
    backend.start()
    init_frontend()  
    backend.join()
