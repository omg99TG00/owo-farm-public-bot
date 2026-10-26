#!/bin/bash
pip uninstall discord.py -y --quiet 2>/dev/null || true
pip install discord.py-self
exec python3 -u main.py
