from os import path, makedirs
from json import dumps, load
from io import open
from pathlib import Path
from typing import Any
from shutil import copytree, rmtree
from secrets import token_hex

from src.utils import wrap_path 

class Settings:
    '''to add a new settings, just add a new item to the list. Reading and writing will detect the change on next launch.'''

    def __init__ (self):
        self.db_path = str(path.join(path.expanduser('~'), 'Documents', 'DB'))
        self.out_path = str(path.join(path.expanduser('~'), 'Desktop', 'TWMA Files'))
        self._log_path = str(path.join(wrap_path("logs", src_level=True))) 
        self._settings_path = path.join(wrap_path("settings", src_level=True), "opt.conf")
        self._secret_key = 0
        self._version = 0.1

        self._read_settings()
    
    def _write_default_settings(self):
      makedirs(path.dirname(self._settings_path), exist_ok=True)
      self.save_settings()

    def get_secret_key(self):
       return self._secret_key
    
    def _read_settings(self):
      if not Path(self._settings_path).exists():
         self._secret_key = token_hex(16)
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
          setattr(self, k, json[k])

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
    
    def _update_fields (self, data: dict[str, Any]):
       for [opt, _] in vars(self).items():
          if data.get(opt) and self.is_public_setting(opt):
             setattr(self, opt, data[opt])
    
    def _create_new_fps (self, data: dict[str, Any]):
       for [opt, fp] in vars(self).items():
          if data.get(opt) and self.is_public_setting(opt):
             copytree(src=fp, dst=data[opt], dirs_exist_ok=True)

    def _cleanup_old_fps (self, data: dict[str, Any]):
       for [opt, fp] in vars(self).items():
          if data.get(opt) and self.is_public_setting(opt):
             rmtree(fp, ignore_errors=True)
      
    def update_settings (self, data: dict[str, Any]):
      # not allowed to make fps and some don't exist already
      if (bad_fps := self.check_filepaths(data)) and not data['create_fps']:
         return f'The following filepaths did not exist and cannot be created:/n{'/n'.join(bad_fps)}'
      
      if data.get('create_fps'):
         self._create_new_fps(data)

      if data.get('remove_old'):
         self._cleanup_old_fps(data)

      self._update_fields(data)
      self.save_settings()