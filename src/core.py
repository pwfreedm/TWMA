from queue import Queue, ShutDown
from flask import Flask

from src.utils import wrap_path 
from src.settings import Settings

app = Flask(
    __name__,
    template_folder=wrap_path("templates"),
    static_folder=wrap_path("static"),
)

class Core():
   """DO NOT create a new instance, use the provided app_core instead
      from src.core import app_core

      apparently this is the standard of 'idiomatic python' over a singleton. 
      feels like 'idiotic python' to me.
      """
   _forms: Queue[dict]
   settings: Settings

   def __init__(self):
      self._forms = Queue(maxsize = 10)
      self.settings = Settings()

   def enqueue(self, form: dict[str, str]):
      self._forms.put(form)
   
   def dequeue(self) -> dict[str, str] | None:
      try:
         return self._forms.get()
      except ShutDown:
         return None

   def shutdown(self):
      self._forms.shutdown()


app_core = Core()
