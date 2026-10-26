#!/bin/bash
rm -rf /home/container/.local/lib/python3.14/site-packages/discord* 2>/dev/null || true
pip uninstall discord.py discord.py-self -y --quiet 2>/dev/null || true
pip install --no-cache-dir discord.py-self
exec python3 -u main.py
