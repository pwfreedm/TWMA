from os import path, makedirs
from json import dumps, load
from io import open
from pathlib import Path
from typing import Any
from shutil import copytree, rmtree

from src.utils import wrap_path 

class Settings:
    '''to add a new settings, just add a new item to the list. Reading and writing will detect the change on next launch.'''

    def __init__ (self):
        self.db_path = str(path.join(path.expanduser('~'), 'Documents', 'DB'))
        self.out_path = str(path.join(path.expanduser('~'), 'Desktop', 'TWMA Files'))
        self._log_path = str(path.join(wrap_path("logs", src_level=True))) 
        self._settings_path = path.join(wrap_path("settings", src_level=True), "opt.conf")
        self._version = 0.1

        self._read_settings()
    
    def _write_default_settings(self):
      makedirs(path.dirname(self._settings_path), exist_ok=True)
      self.save_settings()

    def _read_settings(self):
      if not Path(self._settings_path).exists():
         self._write_default_settings()
         self.unpack_json()

    def save_settings(self):
       file = open(self._settings_path, mode='w')
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

    def check_filepaths (self, data: dict[str, Any]) -> list[str]:
       bad_fps = []
       for [opt, _] in vars(self).items():
          if opt[0] == '_':
             continue
          if not path.exists(data[opt]):
             bad_fps.append(data[opt])
       return bad_fps

    def is_public_setting (self, setting: str):
       return setting[0] != '_'
    
    def update_settings (self, data: dict[str, Any]):
      # not allowed to make fps and some don't exist already
      if (bad_fps := self.check_filepaths(data)) and not data['create_fps']:
         return f'The following filepaths did not exist and cannot be created:/n{'/n'.join(bad_fps)}'
      
      for [opt, fp] in vars(self).items():
         try:
            if data[opt] and self.is_public_setting(opt):
               copytree(fp, data[opt])
               if (data['remove_old']):
                  rmtree(fp)
               vars(self).update({opt : data[opt]})
         except Exception as e:
            return str(e)
         
         self.save_settings()
         return 'success'