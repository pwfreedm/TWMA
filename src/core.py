from queue import Queue, ShutDown
from os import path, makedirs
from json import dumps, load
from flask import Flask
from io import open
from pathlib import Path

from src.utils import wrap_path 

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
   db_path = str(path.join(path.expanduser('~'), 'Documents', 'DB'))
   out_path = str(path.join(path.expanduser('~'), 'Desktop'))
   log_path = str(path.join(wrap_path("logs", src_level=True))) 
   _settings_path = path.join(wrap_path("settings", src_level=True), "opt.conf")

   def __init__(self):
      self._forms = Queue(maxsize = 10)
      self._read_settings()

   def _read_settings(self):
      if not Path(self._settings_path).exists():
         self._write_default_settings()
      opts = load(open(self._settings_path, mode='r'))
      self.db_path = opts['db_path']
      self.out_path = opts['out_path']
      self.log_path = opts['log_path']


   def _write_default_settings(self):
      #TODO: use reflection here to allow easier addition of default filepaths.
      json = dumps({'db_path':self.db_path, 'out_path':self.out_path, 'log_path': self.log_path}, 
                   sort_keys=True, 
                   indent=2, 
                   separators=(',', ':')
                  )
      
      makedirs(path.dirname(self._settings_path), exist_ok=True)
      file = open(self._settings_path, mode='x')
      file.write(json)
      file.close()

      
      


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
