#!/usr/bin/env bash

pyinstaller            \
 --onedir --windowed   \
 --noconfirm --clean   \
 --collect-all PyQt6   \
 --collect-all PyQt6.QtWebEngineWidgets \
 TWMA.py
