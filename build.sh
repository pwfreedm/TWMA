#!/usr/bin/env bash

source $PWD/.venv/bin/activate

pip install -r requirements.txt

pyinstaller \
  --onedir --windowed \
  --noconfirm --clean \
  --add-data="src/static/js:./static/js" \
  --add-data="src/static:./static" \
  --add-data="src/templates:./templates" \
  --add-data="blanks:./blanks" \
  --collect-all PyQt6 \
  --collect-all PyQt6.QtWebEngineWidgets \
  --icon="settings/icon.icns" \
  TWMA.py
