#!/usr/bin/env bash

pyinstaller TWMA.py    \
 --onedir --windowed   \
 --collect-all PyQt6   \
