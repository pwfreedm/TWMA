from queue import Queue, ShutDown
from threading import Event
from src.db import Client, Patient, Appointment, Vet

   
class Core():
   """DO NOT create a new instance, use the provided app_core instead
      from src.core import app_core

      apparently this is the standard of 'idiomatic python' over a singleton. 
      feels like 'idiotic python' to me.
      """
   _forms: Queue[dict]

   def __init__(self):
      self._forms = Queue(maxsize = 10)

   def enqueue(self, form: dict[str, str]):
      self._forms.put(form)
   
   def dequeue(self) -> dict[str, str] | None:

      #'notifying' all threads apparently means just issuing a shutdown error. 
      #catch it and return none to terminate the loop processing forms.
      try:
         return self._forms.get()
      except ShutDown:
         return None
   
   def shutdown(self):
      self._forms.shutdown()

app_core = Core()

def parse_form(form: dict[str, str]) -> tuple[Client, Patient, Appointment, Vet]:
    return tuple(
        [
            Client(form['client'], form['email'], form['phone'], address(form['address'], form['city'], form['state'], form['zip'])),
            Patient(form['patient'], form['animal'], form['sex'], form['weight'], form['disposal'], form['prints'], form['age'], form['breed'], form['color'], form['notes']),
            Appointment(form['date'], form['time']),
            Vet(form['vet'])
        ]
    )