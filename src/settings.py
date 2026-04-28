from os import path, makedirs
from json import dumps, load
from io import open
from pathlib import Path
from typing import Any

from src.utils import wrap_path 

class Settings:
    '''to add a new settings, just add a new item to the list. Reading and writing will detect the change on next launch.'''

    def __init__ (self):
        self.db_path = str(path.join(path.expanduser('~'), 'Documents', 'DB'))
        self.out_path = str(path.join(path.expanduser('~'), 'Desktop'))
        self.log_path = str(path.join(wrap_path("logs", src_level=True))) 
        self._settings_path = path.join(wrap_path("settings", src_level=True), "opt.conf")
        self.version = 0.1

        self._read_settings()
    
    def _write_default_settings(self):
      makedirs(path.dirname(self._settings_path), exist_ok=True)
      self.save_settings()

    def _read_settings(self):
      if not Path(self._settings_path).exists():
         self._write_default_settings()
         self.unpack_json()

    def save_settings(self):
       file = open(self._settings_path, mode='x')
       file.write(self.pack_json())
       file.close()

    def pack_json (self) -> str:
      '''pack this object into a single json string, then return it'''
      return dumps(vars(self), 
                   sort_keys=True, 
                   indent=2, 
                   separators=(',', ':')
        )
    
    def unpack_json(self):
       json = load(open(self._settings_path, mode='r'))
       for [k, _] in vars(self).items():
          self.__setattr__(k, json[k])

    def update_settings (self, data: dict[str, Any]):
       #TODO: when there's a settings form, this will take that form (data) and update fields accordingly.
       pass       
