from shutil import copytree, rmtree, copyfile
from zipfile import ZipFile
import requests 
import os
import subprocess
from io import BytesIO
from pathlib import Path

from src.core import app_core
from src.utils import wrap_path, online


def downlaod_update():
    url = "https://github.com/pwfreedm/TWMA/archive/refs/heads/main.zip"
    repo = requests.get(url, timeout=5)
    with ZipFile(BytesIO(repo.content), 'r') as zip:
        p = wrap_path("update")
        os.makedirs(p, exist_ok=True)
        zip.extractall(path=p)

def install_patch():
    updatable_fps: list[str] = ['src', 'blanks', 'TWMA.py', 'requirements.txt', 'build.sh', 'settings/icon.icns', 'settings/version.conf']
    src_fp = wrap_path("update/TWMA-main", src_level=True)
    for path in updatable_fps:
        if Path(path).is_dir():
            copytree(src=os.path.join(src_fp, path), dst=wrap_path(path, src_level=True), dirs_exist_ok=True)
        else:
            copyfile(src=os.path.join(src_fp, path), dst=wrap_path(path, src_level=True))
            
    subprocess.Popen([f'{os.getcwd()}/build.sh'],
                     stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL)
    rmtree(wrap_path("update", src_level=True))

def needs_update ():
    if not online():
        return False
    local_version = app_core.settings.check_local_version()
    cloud_version = app_core.settings.check_remote_version()
    return local_version < cloud_version
