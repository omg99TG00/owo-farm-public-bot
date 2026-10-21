"""
GhoSty OwO V4 — Modal Panel Edition
Controller: Discord.py with single .panel prefix command
Workers: discord.py-self (selfbot) 
Modal panels for token and channel configuration
Auto-starts workers on valid configuration
"""

import os as brutality_ghosty
import sys
import re
import json as ghostop
import threading
import asyncio
import time as _time
import logging
from datetime import datetime, timedelta

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ---------------------------------------------------------------------------
# Single File Deployment - Embedded Modules
# ---------------------------------------------------------------------------
import base64 as _b64
import zlib as _zlib

_BASE_DIR = brutality_ghosty.path.dirname(brutality_ghosty.path.abspath(__file__))

def _write_if_changed(rel_path, data):
    full_path = brutality_ghosty.path.join(_BASE_DIR, *rel_path.split("/"))
    brutality_ghosty.makedirs(brutality_ghosty.path.dirname(full_path), exist_ok=True)
    if brutality_ghosty.path.exists(full_path):
        with open(full_path, "rb") as _existing:
            if _existing.read() == data:
                return
    with open(full_path, "wb") as _out:
        _out.write(data)

def _materialize_embedded_files():
    for rel_path, text in _EMBEDDED_TEXT.items():
        _write_if_changed(rel_path, text.encode("utf-8"))
    for rel_path, blob in _EMBEDDED_BIN.items():
        _write_if_changed(rel_path, _zlib.decompress(_b64.b64decode(blob)))

_EMBEDDED_TEXT = {
    'core/__init__.py': r'''# https://discord.gg/asMJGgDA7u

"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty OwO V4 Alpha Build
Stable Alpha Build Version: 280826.4.1.0

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""''',
    'core/bossmodule.py': r'''"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty OwO V4 Alpha Build
Stable Alpha Build Version: 280826.4.1.0

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

import asyncio as made_by_ghosty
import random as ghostyjija
from datetime import datetime, timedelta
import math

from .ui import log_worker_event

def calculate_boss_delay():
    min_delay = 17 * 60  
    max_delay = 31 * 60 

    u = max(0.0001, ghostyjija.random())
    v = ghostyjija.random() 
    z = math.sqrt(-2.0 * math.log(u)) * math.cos(2.0 * math.pi * v)
    
    skewed_val = (z * 0.2) + 0.4 

    t = max(0.0, min(1.0, skewed_val))

    p0, p1, p2, p3 = 0.0, 0.2, 0.8, 1.0
    bezier_t = (1-t)**3 * p0 + 3*((1-t)**2)*t * p1 + 3*(1-t)*(t**2) * p2 + t**3 * p3

    delay_range = max_delay - min_delay
    final_delay_seconds = min_delay + (bezier_t * delay_range)
    
    return final_delay_seconds

async def _monitor_boss_fights(ctx, ws, bot):
    await made_by_ghosty.sleep(5)
    log_worker_event(ws.worker_number, "⚔️ Boss module initialized.", "INFO")
    
    first_run = True
    
    while ws.running:
        if getattr(ws, "boss_tickets", 0) <= 0:
            log_worker_event(ws.worker_number, "🚫 Out of boss tickets. Boss module sleeping until restart.", "WARNING")
            break
            
        if first_run:

            delay = ghostyjija.uniform(120.0, 300.0)
            first_run = False
        else:
            delay = calculate_boss_delay()
            
        ws.next_boss_fight_time = datetime.now() + timedelta(seconds=delay)
        log_worker_event(ws.worker_number, f"⏳ Next boss check scheduled in {int(delay//60)}m {int(delay%60)}s (at {ws.next_boss_fight_time.strftime('%H:%M:%S')}).", "DEBUG")
        
        slept = 0
        while slept < delay:
            if not ws.running:
                return
            await made_by_ghosty.sleep(5)
            slept += 5
            
        if not ws.running or getattr(ws, "boss_tickets", 0) <= 0:
            break
            
        await execute_boss_fight(ctx, ws, bot)

async def execute_boss_fight(ctx, ws, bot):
    guild_id = 420104212895105044
    primary_channel_id = 1412234015578132511
    backup_channels = [1412269279398596728, 1412269382599704691]
    owo_bot_id = 408785106942164992
    
    guild = bot.get_guild(guild_id)
    if not guild:
        log_worker_event(ws.worker_number, f"⚠️ Not in target server ({guild_id}). Skipping boss fight.", "DEBUG")
        return
        
    channel = bot.get_channel(primary_channel_id)
    if not channel:
        for backup in backup_channels:
            channel = bot.get_channel(backup)
            if channel:
                break
                
    if not channel:
        log_worker_event(ws.worker_number, "⚠️ Cannot access any boss channels. Skipping boss fight.", "DEBUG")
        return

    log_worker_event(ws.worker_number, "⚔️ Attempting to find a Guild Boss...", "INFO")

    ws.is_boss_fighting = True
    
    try:
        import discord
        from discord.interactions import _wrapped_interaction
        from discord.utils import _generate_nonce
        from discord.enums import InteractionType

        def find_fight_button(data, targets):
            if isinstance(data, dict):
                lbl = str(data.get('label', '')).lower().strip()
                cid = str(data.get('custom_id', '')).lower().strip()
                if data.get('type') == 2 and ('fight' in lbl or 'fight' in cid):
                    if not data.get('disabled', False):
                        targets.append(data)
                    else:
                        log_worker_event(ws.worker_number, "🔍 Found 'Fight' button in raw JSON, but it is disabled.", "DEBUG")
                for v in data.values():
                    find_fight_button(v, targets)
            elif isinstance(data, list):
                for item in data:
                    find_fight_button(item, targets)

        target_message = None
        target_button = None
        
        async for msg in channel.history(limit=40):
            if msg.author.id == owo_bot_id:
                try:
                    route = discord.http.Route("GET", "/channels/{channel_id}/messages?limit=1&around={message_id}", channel_id=channel.id, message_id=msg.id)
                    raw_data = await bot.http.request(route)
                    if isinstance(raw_data, list) and len(raw_data) > 0:
                        raw_data = raw_data[0]
                    
                    if 'components' in raw_data:
                        raw_str = str(raw_data).lower()
                        if "boss" in raw_str or "fight" in raw_str:
                            targets = []
                            find_fight_button(raw_data.get('components', []), targets)
                            if targets:
                                target_message = msg
                                target_button = targets[0]
                                break
                except Exception as e:
                    pass
                
        if not target_button:
            log_worker_event(ws.worker_number, "❌ No active Guild Boss fights found.", "INFO")
            ws.is_boss_fighting = False
            return
            
        log_worker_event(ws.worker_number, "💥 Found Boss! Clicking Fight...", "SUCCESS")
        await _wrapped_interaction(
            target_message._state,
            _generate_nonce(),
            InteractionType.component,
            None,
            channel,
            target_button,
            message=target_message
        )
        
        def check(i):
            if i.user.id == bot.user.id and i.channel.id == channel.id:
                return True
            return False

        try:
            def check_msg(m):
                if m.channel.id == channel.id and getattr(m, 'flags', None) and m.flags.ephemeral:
                    return True
                return False
                
            resp = await bot.wait_for('message', check=check_msg, timeout=5.0)
            content = str(resp.content).lower()
            if not content and resp.embeds:
                for embed in resp.embeds:
                    if embed.description:
                        content += embed.description.lower()
                    if embed.title:
                        content += embed.title.lower()

            if "you don't have any boss tickets" in content:
                log_worker_event(ws.worker_number, "🚫 Out of boss tickets (Discord response).", "WARNING")
                ws.boss_tickets = 0
            elif "you already fought this boss" in content:
                log_worker_event(ws.worker_number, "⚠️ Already fought this boss. Skipping.", "DEBUG")
            else:
                log_worker_event(ws.worker_number, "✅ Boss fight interaction complete.", "SUCCESS")
                
        except made_by_ghosty.TimeoutError:
            log_worker_event(ws.worker_number, "✅ Boss fight clicked (no error messages received).", "SUCCESS")
            
    except Exception as e:
        log_worker_event(ws.worker_number, f"⚠️ Error executing boss fight: {e}", "WARNING")
    finally:
        ws.is_boss_fighting = False
''',
    'core/ghostycorehb.py': r'''"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty OwO V4 Alpha Build
Stable Alpha Build Version: 280826.4.1.0

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

# DO NOT CHANGE THIS FILE UNLESS YOU KNOW WHAT YOU'RE DOING 

import os
import requests
from PIL import Image
import numpy as np
from io import BytesIO

def GhoStyGetImgPaths(directory):
    results = []
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.png'):
                results.append(os.path.join(root, file))
    
    return results

def CompareAllImgsGhoStys(large_data, large_w, small_data, small_w, small_h, start_x, start_y):
    for y in range(small_h):
        for x in range(small_w):
            large_idx = ((start_y + y) * large_w + (start_x + x)) * 4
            small_idx = (y * small_w + x) * 4
            if (small_data[small_idx + 3] > 0 and 
                (small_data[small_idx] != large_data[large_idx] or
                 small_data[small_idx + 1] != large_data[large_idx + 1] or
                 small_data[small_idx + 2] != large_data[large_idx + 2])):
                return False
    
    return True

def MatchGhoStyCapLetters(large_data, large_w, large_h, checks):
    matches = []
    for check in checks:
        img_data = check['img_data']
        small_w = check['width']
        small_h = check['height']
        letter = check['letter']
        
        for y in range(large_h - small_h + 1):
            for x in range(large_w - small_w + 1):
                if CompareAllImgsGhoStys(large_data, large_w, img_data, small_w, small_h, x, y):
                    overlaps = any(
                        abs(match['x'] - x) < small_w and abs(match['y'] - y) < small_h
                        for match in matches
                    )
                    
                    if not overlaps:
                        matches.append({'x': x, 'y': y, 'letter': letter})
    matches.sort(key=lambda m: m['x'])
    return ''.join(match['letter'] for match in matches)

async def GhoStySolveNormalCap(captcha_url):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    letters_dir = os.path.join(current_dir, "letters")
    checks = []
    check_images = sorted(GhoStyGetImgPaths(letters_dir))
    
    for check_image_path in check_images:
        with Image.open(check_image_path) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            width, height = img.size
            img_array = np.array(img)
            img_data = img_array.flatten().astype(np.uint8)
            letter = os.path.splitext(os.path.basename(check_image_path))[0]
            
            checks.append({
                'img_data': img_data,
                'width': width,
                'height': height,
                'letter': letter
            })
    response = requests.get(captcha_url)
    response.raise_for_status()
    with Image.open(BytesIO(response.content)) as large_img:
        if large_img.mode != 'RGBA':
            large_img = large_img.convert('RGBA')
        
        width, height = large_img.size
        large_array = np.array(large_img)
        large_data = large_array.flatten().astype(np.uint8)
    return MatchGhoStyCapLetters(large_data, width, height, checks)

def GhoStySyncedCaptchaSolve(captcha_url):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    letters_dir = os.path.join(current_dir, "letters")
    checks = []
    check_images = sorted(GhoStyGetImgPaths(letters_dir))
    for check_image_path in check_images:
        with Image.open(check_image_path) as img:
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            width, height = img.size
            img_array = np.array(img)
            img_data = img_array.flatten().astype(np.uint8)
            letter = os.path.splitext(os.path.basename(check_image_path))[0]
            
            checks.append({
                'img_data': img_data,
                'width': width,
                'height': height,
                'letter': letter
            })
    

    response = requests.get(captcha_url)
    response.raise_for_status()
    

    with Image.open(BytesIO(response.content)) as large_img:

        if large_img.mode != 'RGBA':
            large_img = large_img.convert('RGBA')
        
        width, height = large_img.size

        large_array = np.array(large_img)
        large_data = large_array.flatten().astype(np.uint8)
    return MatchGhoStyCapLetters(large_data, width, height, checks)

if __name__ == "__main__":
    pass''',
    'core/heart.py': r'''"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty OwO V4 Alpha Build
Stable Alpha Build Version: 280826.4.1.0

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

import random as ghostyjija
import time
import re
import os
import unicodedata
import threading
import json as ghostop
import asyncio as made_by_ghosty
from datetime import datetime, timedelta
from .modules import parse_zoo_message, fetch_zoo_data, format_value, parse_gems, SPEED_MODES
from .ghostycorehb import GhoStySolveNormalCap, GhoStySyncedCaptchaSolve
from .ui import log_worker_event, log_critical, log_support_prompt
from .bossmodule import _monitor_boss_fights

class WorkerState:
    def __init__(self, worker_number):
        self.worker_number = worker_number
        self.bot = None
        self.username = "Unknown"
        self.running = False
        self.has_started = False
        self.sleep_mode = False
        self.farming_start_time = None
        self.sleep_start_time = None
        self.ghosty_start_time = datetime.now()
        self.ghosty_commands_sent = 0
        self.ghosty_gems_used = 0
        self.last_gem_check = 0
        self.current_speed_mode = "lifetime"
        self.last_mode_change_time = datetime.now()
        self.lifetime_work_cycles = 0
        self.lifetime_day_skip_active = False
        self.lifetime_cycle_start_time = None
        self.initial_cash = 0
        self.initial_essence = 0
        self.current_cash = 0
        self.current_essence = 0
        self.zoo_channel = None
        self.GhoStyHbAlrActiveVar = False
        self.GhoStyCoreAvailCheck = True
        self.huntbot_enabled = True        
        self.active_channel_id = None
        self.auto_start_channel_id = None    
        self.paused = False                  
        self.pause_end_time = None          
        self.boss_tickets = 3
        self.is_boss_fighting = False
        self.next_boss_fight_time = None
        self.is_mail_claiming = False
        self.last_mail_claim = None
        
    def to_dict(self):
        def serialize_dt(dt):
            return dt.isoformat() if dt else None
            
        return {
            "worker_number": self.worker_number,
            "username": self.username,
            "running": self.running,
            "has_started": self.has_started,
            "sleep_mode": self.sleep_mode,
            "paused": self.paused,
            "current_speed_mode": self.current_speed_mode,
            "initial_cash": self.initial_cash,
            "initial_essence": self.initial_essence,
            "ghosty_commands_sent": self.ghosty_commands_sent,
            "ghosty_gems_used": self.ghosty_gems_used,
            "farming_start_time": serialize_dt(self.farming_start_time),
            "pause_end_time": serialize_dt(self.pause_end_time),
            "sleep_start_time": serialize_dt(self.sleep_start_time),
            "ghosty_start_time": serialize_dt(self.ghosty_start_time),
            "lifetime_work_cycles": self.lifetime_work_cycles,
            "lifetime_day_skip_active": self.lifetime_day_skip_active,
            "lifetime_cycle_start_time": serialize_dt(self.lifetime_cycle_start_time),
            "huntbot_enabled": self.huntbot_enabled,
            "huntbot_solver_available": self.GhoStyCoreAvailCheck,
            "last_gem_check": self.last_gem_check,
            "boss_tickets": self.boss_tickets,
            "is_boss_fighting": self.is_boss_fighting,
            "next_boss_fight_time": serialize_dt(self.next_boss_fight_time),
            "is_mail_claiming": self.is_mail_claiming,
            "last_mail_claim": serialize_dt(self.last_mail_claim)
        }

class WorkerManager:
    _instance = None
    _lock = threading.Lock()

    HB_DATA_FILE = "ghostyhbworkers.json"

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._workers = {}
                cls._instance._channel_locks = {}
                cls._instance._main_token = None
                cls._instance._total_workers = 0
                cls._instance._hb_lock = threading.Lock()
                cls._instance._has_channels_config = False  # NEW
            return cls._instance

    def register_worker(self, state):
        with self._lock:
            self._workers[state.worker_number] = state
            self._total_workers = len(self._workers)

    def get_worker(self, worker_number):
        with self._lock:
            return self._workers.get(worker_number)

    def get_all_workers(self):
        with self._lock:
            return dict(self._workers)

    def set_main_token(self, token):
        self._main_token = token

    def set_has_channels_config(self, value: bool):
        self._has_channels_config = value

    @property
    def has_channels_config(self):
        return self._has_channels_config

    @property
    def main_token(self):
        return self._main_token

    @property
    def total_workers(self):
        return self._total_workers

    def try_claim_channel(self, channel_id, worker_number):
        with self._lock:
            existing = self._channel_locks.get(channel_id)
            if existing is not None and existing != worker_number:
                return False, existing
            self._channel_locks[channel_id] = worker_number
            return True, None

    def release_channel(self, channel_id, worker_number):
        with self._lock:
            if self._channel_locks.get(channel_id) == worker_number:
                del self._channel_locks[channel_id]

    def get_channel_worker(self, channel_id):
        with self._lock:
            return self._c
