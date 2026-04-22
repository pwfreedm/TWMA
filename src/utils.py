import sys as sys
from os import path, getcwd
from pathlib import Path

def address (street: str, city: str, state: str, zip: str) -> str: 
   return street + ', ' + city + ', ' + state + ' ' + zip if len(street) > 0 else ""

def wrap_path(relative_path: str, is_pdf = False) -> Path:
    """if running the app through pyinstaller, this will replace a path of ./something with pyinstaller root/something"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        #its this or packaging for nix.
        if is_pdf:
            base_path = getcwd()
        else:
            base_path = path.join(getcwd(), 'src')
    return path.join(base_path, relative_path)