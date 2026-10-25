"""
GhoSty OwO V4 — Public Multi-User Modal Panel Edition
Per-user configuration with real-time validation
TOKEN-CHANNELID format in single modal
User-isolated worker management
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
from typing import Dict, List, Tuple, Optional

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
# EMBEDDED MODULES
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

# PLACEHOLDER - will be injected with actual embedded content
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
            return self._channel_locks.get(channel_id)

    def try_claim_friend_battle_helper(self, requester_number):
        with self._lock:
            requester = self._workers.get(requester_number)
            if not requester or getattr(requester, 'busy_with_quest', False):
                return None
                
            for w_num, w_state in self._workers.items():
                if w_num != requester_number:
                    is_busy = getattr(w_state, 'busy_with_quest', False)
                    if w_state.running and not w_state.paused and not w_state.sleep_mode and not is_busy:
                        # Claim both!
                        requester.busy_with_quest = True
                        w_state.busy_with_quest = True
                        return w_state
            return None

    def get_action_helpers(self, requester_number, count):
        with self._lock:
            helpers = []
            now = time.time()
            for w_num, w_state in self._workers.items():
                if w_num == requester_number:
                    continue
                if not w_state.running:
                    continue
                last_action_time = getattr(w_state, 'last_action_helper_time', 0)
                if now - last_action_time < 3.0:
                    continue
                
                w_state.last_action_helper_time = now
                helpers.append(w_state)
                if len(helpers) >= count:
                    break
            return helpers

    def get_cookie_helpers(self, requester_number, count):
        with self._lock:
            helpers = []
            now = datetime.now()
            for w_num, w_state in self._workers.items():
                if w_num == requester_number:
                    continue
                if not w_state.running:
                    continue
                
                reset_time = getattr(w_state, 'cookie_reset_time', datetime.min)
                if now < reset_time:
                    continue
                
                w_state.cookie_reset_time = now + timedelta(minutes=5)
                helpers.append(w_state)
                if len(helpers) >= count:
                    break
            return helpers

    def get_pray_curse_helpers(self, requester_number, count):
        with self._lock:
            helpers = []
            now = datetime.now()
            for w_num, w_state in self._workers.items():
                if w_num == requester_number:
                    continue
                if not w_state.running:
                    continue
                reset_time = getattr(w_state, 'pray_curse_reset_time', datetime.min)
                if now < reset_time:
                    continue
                
                w_state.pray_curse_reset_time = now + timedelta(minutes=5, seconds=10)
                helpers.append(w_state)
                if len(helpers) >= count:
                    break
            return helpers

    def load_hb_data(self, worker_number):
        with self._hb_lock:
            try:
                if os.path.exists(self.HB_DATA_FILE):
                    with open(self.HB_DATA_FILE, "r") as f:
                        all_data = ghostop.load(f)
                    return all_data.get(str(worker_number), {})
            except:
                pass
        return {}

    def save_hb_data(self, worker_number, data):
        with self._hb_lock:
            all_data = {}
            try:
                if os.path.exists(self.HB_DATA_FILE):
                    with open(self.HB_DATA_FILE, "r") as f:
                        all_data = ghostop.load(f)
            except:
                pass
            all_data[str(worker_number)] = data
            with open(self.HB_DATA_FILE, "w") as f:
                ghostop.dump(all_data, f, indent=4)


manager = WorkerManager()

def ParseGhoStyTimeStrs(time_str):
    time_str = time_str.upper().strip()
    h = int(re.search(r'(\d+)H', time_str).group(1)) if 'H' in time_str else 0
    m = int(re.search(r'(\d+)M', time_str).group(1)) if 'M' in time_str else 0
    return timedelta(hours=h, minutes=m)


def LoadGhoStysHbData(ws):
    return manager.load_hb_data(ws.worker_number)


def SaveHbDataGhoStys(ws, data):
    manager.save_hb_data(ws.worker_number, data)


def GhoStyEmbedParser(msg_content):
    try:
        content = msg_content.lower().replace(",", "")
        match = re.search(r"current max autohunt:.*?for (\d+) cowoncy", content)
        if match:
            return int(match.group(1))
    except:
        pass
    return 20000


async def GhoStyCapUrlSolver(url):
    try:
        if GhoStySolveNormalCap:
            try:
                return await GhoStySolveNormalCap(url)
            except:
                pass
        if GhoStySyncedCaptchaSolve:
            try:
                return GhoStySyncedCaptchaSolve(url)
            except:
                pass
    except:
        pass
    return None


async def CheckGhoStyHbMsgFetch(ctx, ws, cowoncy_amount=None):
    if not ws.huntbot_enabled:
        return False

    try:
        await made_by_ghosty.sleep(1)
        messages = [msg async for msg in ctx.channel.history(limit=5)]

        for msg in messages:
            if msg.author.id != 408785106942164992:
                continue

            msg_content = str(msg.content)
            if not msg_content and msg.embeds:
                embed = msg.embeds[0]
                msg_content = (embed.description or "") + "".join(
                    f"{f.name}\n{f.value}" for f in embed.fields
                )
            msg_content_lower = msg_content.lower()

            if "beep. boop. i am huntbot" in msg_content_lower:
                optimal_cowoncy = GhoStyEmbedParser(msg_content)
                log_worker_event(ws.worker_number, f"HuntBot: Found optimal cowoncy: {optimal_cowoncy}", "INFO")
                data = LoadGhoStysHbData(ws)
                data["optimal_cowoncy"] = optimal_cowoncy
                data["channel_id"] = ctx.channel.id
                SaveHbDataGhoStys(ws, data)
                await made_by_ghosty.sleep(2)
                await ctx.send(f"owo hb {optimal_cowoncy}")
                await made_by_ghosty.sleep(4)
                return await CheckGhoStyHbMsgFetch(ctx, ws, optimal_cowoncy)

            if "i will be back in" in msg_content_lower:
                match = re.search(r"i will be back in (\d+h\s*\d*m?|\d+m)", msg_content_lower)
                if match:
                    time_str = match.group(1).strip()
                    delta = ParseGhoStyTimeStrs(time_str)
                    next_time = datetime.now() + delta
                    data = LoadGhoStysHbData(ws)
                    data.update({
                        "next_huntbot_time": next_time.isoformat(),
                        "is_hunting": True,
                        "last_updated": datetime.now().isoformat(),
                        "channel_id": ctx.channel.id,
                    })
                    SaveHbDataGhoStys(ws, data)
                    ws.GhoStyHbAlrActiveVar = True
                    log_worker_event(ws.worker_number, f"⏰ Next huntbot in {delta} (at {next_time.strftime('%H:%M:%S')})", "INFO")
                    await ctx.send(f" ⏰ HuntBot will trigger in {delta}")
                    return True

            if "here is your password!" in msg_content_lower and msg.attachments:
                url = msg.attachments[0].url
                log_worker_event(ws.worker_number, f"🔍 Solving captcha from {url}", "DEBUG")
                result = await GhoStyCapUrlSolver(url)
                if result:
                    use_cowoncy = cowoncy_amount or LoadGhoStysHbData(ws).get("optimal_cowoncy", 20000)
                    await made_by_ghosty.sleep(2)
                    await ctx.send(f"owo autohunt {use_cowoncy} {result}")
                    log_worker_event(ws.worker_number, f"✅ Auto-solved HuntBot: `{result}` (Used {use_cowoncy})", "SUCCESS")
                    await made_by_ghosty.sleep(4)
                    return await CheckGhoStyHbMsgFetch(ctx, ws, use_cowoncy)
                else:
                    await ctx.send(" ❌ GhoSty Core Module failed to solve HuntBot. Please join the support server to get help.")
                    return False

            if (
                "you spent" in msg_content_lower
                and "cowoncy" in msg_content_lower
                and "i will be back in" in msg_content_lower
            ):
                match = re.search(r"i will be back in (\d+h\s*\d*m?|\d+m)", msg_content_lower)
                if match:
                    time_str = match.group(1).strip()
                    delta = ParseGhoStyTimeStrs(time_str)
                    next_time = datetime.now() + delta
                    data = LoadGhoStysHbData(ws)
                    data.update({
                        "next_huntbot_time": next_time.isoformat(),
                        "is_hunting": True,
                        "last_updated": datetime.now().isoformat(),
                        "channel_id": ctx.channel.id,
                        "hunt_stage": "waiting_for_return",
                    })
                    SaveHbDataGhoStys(ws, data)
                    ws.GhoStyHbAlrActiveVar = True
                    log_worker_event(ws.worker_number, f"🎯 Hunt started. Will return in {delta}", "INFO")
                    await ctx.send(f"🎯 Hunt active. Bot will return in {delta}")
                    return True

            if "i am back with" in msg_content_lower and "animals" in msg_content_lower:
                log_worker_event(ws.worker_number, "🎉 Hunt completed!", "SUCCESS")
                await ctx.send("🎉 Hunt completed! Restarting HuntBot in 15 seconds")
                await made_by_ghosty.sleep(15)
                await ctx.send("owo hb")
                log_worker_event(ws.worker_number, "📤 Sent: owo hb (after hunt return)", "DEBUG")
                await made_by_ghosty.sleep(4)
                return await CheckGhoStyHbMsgFetch(ctx, ws)

        return False
    except Exception as e:
        log_worker_event(ws.worker_number, f"⚠️ Error in CheckGhoStyHbMsgFetch: {e}", "WARNING")
        return False

async def _do_gem_check(ctx, ws):
    if ws.sleep_mode or ws.paused:
        return
    await ctx.send("owo lb all")
    await made_by_ghosty.sleep(2)
    await ctx.send("owo inventory")
    await made_by_ghosty.sleep(3)
    try:
        latest_messages = [msg async for msg in ctx.channel.history(limit=2)]
        for message in latest_messages:
            if message.author.id == 408785106942164992:
                if "inventory" in message.content.lower():
                    gem_numbers = await parse_gems(message.content)
                    if gem_numbers:
                        use_command = "owo use " + " ".join(gem_numbers)
                        await ctx.send(use_command)
                        ws.ghosty_gems_used += len(gem_numbers)
                        await made_by_ghosty.sleep(3)
                    else:
                        log_worker_event(ws.worker_number, "No gems found in inventory", "DEBUG")
                    break
    except Exception as e:
        log_worker_event(ws.worker_number, f"Error in gem check: {e}", "WARNING")



async def _check_warning(ctx, ws):
    if ws.sleep_mode or ws.paused:
        return False
    try:
        messages = [msg async for msg in ctx.channel.history(limit=10)]
        for msg in messages:
            msg_content = str(msg.content)
            if not msg_content:
                continue
            msg_content_clean = unicodedata.normalize("NFKC", msg_content)
            msg_content_clean = re.sub(r'[\u200B-\u200D\uFEFF]', '', msg_content_clean)
            msg_content_lower = msg_content_clean.lower()

            if "captcha" in msg_content_lower and "verify" in msg_content_lower:
                warning_pattern = r'[\(\[\{]?\s*(\d+)\s*[\/／]\s*5\s*[\)\]\}]?'
                match = re.search(warning_pattern, msg_content_lower)
                if match:
                    warning_count = int(match.group(1))
                    log_worker_event(ws.worker_number, f"⚠️ CAPTCHA WARNING: ({warning_count}/5)", "WARNING")
                    if warning_count == 1:
                        ws.running = False
                        ws.paused = False
                        ws.pause_end_time = None
                        manager.release_channel(ctx.channel.id, ws.worker_number)
                        await ctx.send(
                            "⚠ WARNING DETECTED! 🛑 Stopping | **SOLVE YOUR CAPTCHA FIRST** | "
                            "Then Type `.start` again to restart grinding."
                        )
                        log_worker_event(ws.worker_number, "🛑 Stopped due to CAPTCHA (1/5)", "CRITICAL")
                        return True
        return False
    except Exception as e:
        log_worker_event(ws.worker_number, f"Warning check error: {e}", "WARNING")
        return False


async def _monitor_huntbot(ctx, ws, bot):
    while ws.running:
        if not ws.huntbot_enabled:
            log_worker_event(ws.worker_number, "HuntBot monitor exiting (disabled)", "DEBUG")
            return

        try:
            data = LoadGhoStysHbData(ws)
            if "next_huntbot_time" in data and data.get("channel_id") == ctx.channel.id:
                next_time_str = data["next_huntbot_time"]
                next_time = datetime.fromisoformat(next_time_str)
                current_time = datetime.now()

                if current_time >= next_time and data.get("is_hunting"):
                    log_worker_event(ws.worker_number, "⏰ HuntBot timer reached!", "INFO")
                    await ctx.send("⏰ HuntBot timer reached! Restarting...")
                    data["is_hunting"] = False
                    SaveHbDataGhoStys(ws, data)
                    ws.GhoStyHbAlrActiveVar = False
                    await made_by_ghosty.sleep(2)
                    await ctx.send("owo hb")
                    log_worker_event(ws.worker_number, "📤 Sent: owo hb (auto-triggered)", "DEBUG")
                    await made_by_ghosty.sleep(4)
                    await CheckGhoStyHbMsgFetch(ctx, ws)

            await made_by_ghosty.sleep(30)
        except Exception as e:
            log_worker_event(ws.worker_number, f"⚠️ Error in monitor_huntbot: {e}", "WARNING")
            await made_by_ghosty.sleep(60)


def _parse_pause_time(time_str):

    m = re.fullmatch(r'(?:(\d+)h)?(?:(\d+)m)?', time_str.strip().lower())
    if not m or (not m.group(1) and not m.group(2)):
        return None
    hours = int(m.group(1)) if m.group(1) else 0
    mins = int(m.group(2)) if m.group(2) else 0
    return hours * 3600 + mins * 60


def _format_duration(seconds):
    h, rem = divmod(int(seconds), 3600)
    m = rem // 60
    if h and m:
        return f"{h}h {m}m"
    elif h:
        return f"{h}h"
    else:
        return f"{m}m"


async def setup_user_settings(ctx, ws):
    await made_by_ghosty.sleep(3.4)
    await ctx.send("owo bs")
    await made_by_ghosty.sleep(5.1)
    try:
        import discord
        from discord.interactions import _wrapped_interaction
        from discord.utils import _generate_nonce
        from discord.enums import InteractionType

        def find_buttons(data, targets):
            if isinstance(data, dict):
                if data.get('type') == 2 and str(data.get('label', '')).lower() == 'image':
                    targets.append(data)
                for v in data.values():
                    find_buttons(v, targets)
            elif isinstance(data, list):
                for item in data:
                    find_buttons(item, targets)

        bs_msg = None
        for _ in range(3):
            messages = [msg async for msg in ctx.channel.history(limit=40)]
            for msg in messages:
                if msg.author.id == 408785106942164992:
                    try:
                        route = discord.http.Route("GET", "/channels/{channel_id}/messages?limit=1&around={message_id}", channel_id=ctx.channel.id, message_id=msg.id)
                        raw_data = await ws.bot.http.request(route)
                        if isinstance(raw_data, list) and len(raw_data) > 0:
                            raw_data = raw_data[0]
                        if 'components' in raw_data:
                            raw_str = str(raw_data).lower()
                            if "user settings" in raw_str or "battle display" in raw_str or "custom_id" in raw_str:
                                bs_msg = msg
                                break
                    except Exception:
                        pass
                if bs_msg:
                    break
            
            if bs_msg:
                break
            await made_by_ghosty.sleep(2)

        if not bs_msg:
            log_worker_event(ws.worker_number, "Could not find 'owo bs' response", "DEBUG")
            return

        max_clicks = 10
        clicks = 0
        while clicks < max_clicks:
            route = discord.http.Route("GET", "/channels/{channel_id}/messages?limit=1&around={message_id}", channel_id=ctx.channel.id, message_id=bs_msg.id)
            raw_data = await ws.bot.http.request(route)
            if isinstance(raw_data, list) and len(raw_data) > 0:
                raw_data = raw_data[0]
            
            targets = []
            find_buttons(raw_data.get('components', []), targets)
            
            if not targets:
                log_worker_event(ws.worker_number, "User settings configured (all set to 'text'!)", "SUCCESS")
                break
                
            target = targets[0]
            log_worker_event(ws.worker_number, f"Clicking settings button: {target.get('custom_id')}", "DEBUG")
            
            try:
                await _wrapped_interaction(
                    bs_msg._state,
                    _generate_nonce(),
                    InteractionType.component,
                    None,
                    bs_msg.channel,
                    target,
                    message=bs_msg
                )
            except Exception as e:
                log_worker_event(ws.worker_number, f"Error clicking button: {e}", "WARNING")
                
            clicks += 1
            await made_by_ghosty.sleep(2.5)

    except Exception as e:
        log_worker_event(ws.worker_number, f"Error setting up user settings: {e}", "WARNING")

def _get_humanoid_delay(ws, min_delay, max_delay):
    uptime_mins = (datetime.now() - ws.ghosty_start_time).total_seconds() / 60
    if uptime_mins <= 30:
        fatigue = 0.8
    elif uptime_mins <= 90:
        fatigue = 1.0
    else:
        fatigue = 1.3
        
    base = ghostyjija.gauss(mu=(min_delay + max_delay) / 2, sigma=(max_delay - min_delay) / 4)
    t = (base - min_delay) / (max_delay - min_delay)
    t = max(0.0, min(1.0, t))
    bezier_t = 3 * (t**2) - 2 * (t**3)
    
    final_delay = min_delay + bezier_t * (max_delay - min_delay)
    final_delay *= fatigue
    return max(min_delay * 0.8, min(max_delay * 1.5, final_delay))


async def _run_farming_loop(ctx, ws, bot):
    ws.running = True
    ws.sleep_mode = False
    ws.has_started = True
    ws.paused = False
    ws.pause_end_time = None
    ws.zoo_channel = ctx.channel
    ws.last_gem_check = time.time()
    ws.sleep_start_time = None
    ws.farming_start_time = datetime.now()
    ws.last_mode_change_time = datetime.now()
    ws.ghosty_start_time = datetime.now()
    ws.active_channel_id = ctx.channel.id

    ws.lifetime_work_cycles = 0
    ws.lifetime_day_skip_active = False
    ws.lifetime_cycle_start_time = datetime.now()

    current_config = SPEED_MODES[ws.current_speed_mode]
    zoo_data = await fetch_zoo_data(ctx)
    if zoo_data:
        ws.initial_cash = zoo_data["total_cash"]
        ws.initial_essence = zoo_data["total_essence"]

    await setup_user_settings(ctx, ws)

    if ws.huntbot_enabled:
        await made_by_ghosty.sleep(2)
        data = LoadGhoStysHbData(ws)
        data["channel_id"] = ctx.channel.id
        SaveHbDataGhoStys(ws, data)
        await ctx.send("owo hb")
        await made_by_ghosty.sleep(4)
        await CheckGhoStyHbMsgFetch(ctx, ws)
        bot.loop.create_task(_monitor_huntbot(ctx, ws, bot))
        await made_by_ghosty.sleep(2)
    else:
        log_worker_event(ws.worker_number, "Auto-HuntBot disabled, skipping HB setup", "DEBUG")
    bot.loop.create_task(_monitor_boss_fights(ctx, ws, bot))

    last_command = None

    while ws.running:
        try:
            if ws.paused and not ws.sleep_mode:
                now = datetime.now()
                if now >= ws.pause_end_time:
                    ws.paused = False
                    ws.pause_end_time = None
                    ws.farming_start_time = datetime.now()
                    ws.last_mode_change_time = datetime.now()
                    if ws.lifetime_cycle_start_time is not None:
                        ws.lifetime_cycle_start_time = datetime.now()
                    await ctx.send("⏰ **Pause over!** Resuming farming now.")
                    log_worker_event(ws.worker_number, "⏰ Pause ended, resuming farming", "INFO")
                else:
                    await made_by_ghosty.sleep(10)
                    continue

            if ws.has_started and ws.running and not ws.sleep_mode and not ws.paused:
                current_time = datetime.now()
                
                try:
                    from .questsmodule import check_and_handle_quests
                    await check_and_handle_quests(ctx, ws, bot)
                except Exception as e:
                    log_worker_event(ws.worker_number, f"Error checking quests: {e}", "WARNING")

                if ws.current_speed_mode in ["lifetime", "humanoid"]:
                    current_config = SPEED_MODES[ws.current_speed_mode]

                    if not ws.lifetime_day_skip_active:
                        should_skip_day = ghostyjija.random() < 0.5
                        if ws.lifetime_work_cycles >= ghostyjija.randint(3, 4) and should_skip_day:
                            ws.lifetime_day_skip_active = True
                            day_skip_duration = 24 * 3600
                            skip_end_time = current_time + timedelta(seconds=day_skip_duration)
                            await ctx.send(
                                f"😴 **LIFETIME MODE: DAY SKIP ACTIVATED** 🌙\n"
                                f"Full 24-hour rest. Will resume at **{skip_end_time.strftime('%d-%b-%Y %I:%M:%S %p')}**"
                            )
                            log_worker_event(ws.worker_number, "⏸️ LIFETIME DAY SKIP started", "INFO")
                            await made_by_ghosty.sleep(day_skip_duration)
                            ws.lifetime_day_skip_active = False
                            ws.lifetime_work_cycles = 0
                            ws.farming_start_time = datetime.now()
                            ws.lifetime_cycle_start_time = datetime.now()
                            await ctx.send("⏰ **LIFETIME MODE: RESUMING AFTER DAY SKIP** 🚀")
                            log_worker_event(ws.worker_number, "⏰ LIFETIME DAY SKIP ENDED — resuming", "INFO")
                            continue

                    if ws.lifetime_cycle_start_time is None:
                        ws.lifetime_cycle_start_time = current_time

                    work_duration = ghostyjija.uniform(
                        current_config["work_duration_min"],
                        current_config["work_duration_max"],
                    )
                    elapsed_cycle_time = (current_time - ws.lifetime_cycle_start_time).total_seconds()

                    if elapsed_cycle_time >= work_duration:
                        ws.sleep_mode = True
                        break_duration = ghostyjija.uniform(
                            current_config["break_duration_min"],
                            current_config["break_duration_max"],
                        )
                        ws.sleep_start_time = current_time
                        sleep_end_time = current_time + timedelta(seconds=break_duration)
                        ws.lifetime_work_cycles += 1
                        hours, remainder = divmod(int(break_duration), 3600)
                        mins = remainder // 60
                        await ctx.send(
                            f"😴 **LIFETIME MODE: BREAK TIME** 🌙\n"
                            f"Work cycle #{ws.lifetime_work_cycles} complete. Breaking for {hours}h {mins}m. "
                            f"Resume at **{sleep_end_time.strftime('%d-%b-%Y %I:%M:%S %p')}**"
                        )
                        log_worker_event(ws.worker_number, f"😴 LIFETIME BREAK #{ws.lifetime_work_cycles}: {hours}h {mins}m", "INFO")
                        await made_by_ghosty.sleep(break_duration)
                        ws.sleep_mode = False
                        ws.lifetime_cycle_start_time = datetime.now()
                        if not ws.paused:
                            await ctx.send(
                                f"⏰ **LIFETIME MODE: BACK TO WORK** 🚀\n"
                                f"Starting work cycle #{ws.lifetime_work_cycles + 1}"
                            )
                            log_worker_event(ws.worker_number, f"⏰ LIFETIME WORK CYCLE #{ws.lifetime_work_cycles + 1} started", "INFO")
                        continue

                else:
                    active_mode = ws.current_speed_mode
                    current_config = SPEED_MODES[active_mode]
                    elapsed_time = (current_time - ws.farming_start_time).total_seconds()
                    max_run_time = ghostyjija.uniform(
                        current_config["run_duration_min"],
                        current_config["run_duration_max"],
                    )
                    if elapsed_time >= max_run_time:
                        ws.sleep_mode = True
                        sleep_duration = ghostyjija.uniform(
                            current_config["sleep_duration_min"],
                            current_config["sleep_duration_max"],
                        )
                        ws.sleep_start_time = current_time
                        sleep_end_time = current_time + timedelta(seconds=sleep_duration)
                        await ctx.send(
                            f"😴 Entering sleep mode. Will resume at "
                            f"**{sleep_end_time.strftime('%d-%b-%Y %I:%M:%S %p')}**"
                        )
                        log_worker_event(ws.worker_number, "😴 Sleep mode started", "INFO")
                        await made_by_ghosty.sleep(sleep_duration)
                        ws.sleep_mode = False
                        ws.farming_start_time = datetime.now()
                        ws.last_mode_change_time = datetime.now()
                        if not ws.paused:
                            await ctx.send("⏰ Waking up from sleep. Resuming")
                            log_worker_event(ws.worker_number, "⏰ Waking up from sleep mode, resuming", "INFO")
                        continue

            if ws.sleep_mode:
                await made_by_ghosty.sleep(10)
                continue

            if ws.paused:
                await made_by_ghosty.sleep(10)
                continue

            if getattr(ws, "is_boss_fighting", False):
                await made_by_ghosty.sleep(5)
                continue
                
            if getattr(ws, "is_mail_claiming", False):
                await made_by_ghosty.sleep(5)
                continue

            current_time_ts = time.time()
            current_config = SPEED_MODES[ws.current_speed_mode]

            gem_check_interval = ghostyjija.randint(
                int(current_config["gem_check_interval_min"]),
                int(current_config["gem_check_interval_max"]),
            )

            if current_time_ts - ws.last_gem_check >= gem_check_interval:
                warning_detected = await _check_warning(ctx, ws)
                if warning_detected or not ws.running:
                    break
                await _do_gem_check(ctx, ws)
                ws.last_gem_check = current_time_ts
                continue

            def ghostysmarttypo(command):
                if ghostyjija.random() < 0.12:
                    idx = ghostyjija.randint(0, len(command) - 1)
                    ghostytypochars = ghostyjija.choice("abcdefghijklmnopqrstuvwxyz")
                    return command[:idx] + ghostytypochars + command[idx + 1:]
                return command

            cmds = [
                ghostysmarttypo("owoh"),
                ghostysmarttypo("owo pray"),
                ghostysmarttypo("owo h"),
                ghostysmarttypo("owo b"),
                ghostysmarttypo("owob"),
                ghostysmarttypo("owoh"),
                ghostysmarttypo("owo h"),
                ghostysmarttypo(ghostyjija.choice(["owo cf 1", "owoz", "owo s 2", "owo owo", "owoq"])),
                ghostysmarttypo(ghostyjija.choice(["owo pup", "owo army", "owo piku", "owo run"])),
                ghostysmarttypo(ghostyjija.choice(["owo punch <@408785106942164992>", "owo roll"])),
            ]
            command = ghostyjija.choice(cmds)
            while command == last_command:
                command = ghostyjija.choice(cmds)
            last_command = command

            await ctx.send(command)
            ws.ghosty_commands_sent += 1

            await made_by_ghosty.sleep(current_config["command_delay"])
            warning_detected = await _check_warning(ctx, ws)
            if warning_detected or not ws.running:
                break

            if ws.current_speed_mode == "humanoid":
                delay = _get_humanoid_delay(ws, current_config["action_delay_min"], current_config["action_delay_max"])
                try:
                    if bot and hasattr(bot, 'guilds') and bot.guilds:
                        g = ghostyjija.choice(bot.guilds)
                        channels = [c for c in g.text_channels if c.permissions_for(g.me).view_channel]
                        if channels:
                            c = ghostyjija.choice(channels)
                            _ = [msg async for msg in c.history(limit=5)]
                except Exception:
                    pass
                await made_by_ghosty.sleep(delay)
            else:
                await made_by_ghosty.sleep(
                    ghostyjija.uniform(
                        current_config["action_delay_min"],
                        current_config["action_delay_max"],
                    )
                )
            if ghostyjija.random() < 0.05:
                await made_by_ghosty.sleep(
                    ghostyjija.uniform(
                        current_config["random_long_delay_min"],
                        current_config["random_long_delay_max"],
                    )
                )

        except Exception as e:
            log_worker_event(ws.worker_number, f"Error in main loop: {e}", "CRITICAL")


async def _fetch_zoo_for_main_status(ws):
    if not ws.has_started or not ws.zoo_channel or ws.sleep_mode or ws.paused:
        return
    try:
        await ws.zoo_channel.send("owo zoo")
        await made_by_ghosty.sleep(5)
        messages = [msg async for msg in ws.zoo_channel.history(limit=10)]
        zoo_messages = []
        for msg in messages:
            if msg.author.id == 408785106942164992:
                content_lower = msg.content.lower()
                if (any(kw in content_lower for kw in ["zoo", "animals", "cowoncy", "points:"]) or any(sup in msg.content for sup in "⁰¹²³⁴⁵⁶⁷⁸⁹")):
                    zoo_messages.append(msg.content)
                    if "common" in content_lower:
                        break
        if zoo_messages:
            zoo_messages.reverse()
            zoo_data = await parse_zoo_message(zoo_messages)
            ws.current_cash = zoo_data["total_cash"]
            ws.current_essence = zoo_data["total_essence"]
            log_worker_event(ws.worker_number, "Zoo data fetched for main status", "DEBUG")
    except Exception as e:
        log_worker_event(ws.worker_number, f"Error in main-status zoo fetch: {e}", "WARNING")


async def _send_status(ctx, ws_target, live_fetch=True):
    current_config = SPEED_MODES[ws_target.current_speed_mode]

    if ws_target.paused:
        remaining = ws_target.pause_end_time - datetime.now() if ws_target.pause_end_time else timedelta(0)
        rem_secs = max(0, int(remaining.total_seconds()))
        rem_str = _format_duration(rem_secs) if rem_secs > 0 else "ending soon"
        if ws_target.sleep_mode:
            ghosty_state = f"⏸️ Paused (after current sleep) — {rem_str} remaining"
        else:
            ghosty_state = f"⏸️ Paused — {rem_str} remaining"
    elif ws_target.current_speed_mode == "lifetime":
        if ws_target.lifetime_day_skip_active:
            ghosty_state = f"🌙 Day Skip Mode ({current_config['name']})"
        elif ws_target.sleep_mode:
            ghosty_state = f"😴 Break Time (Cycle #{ws_target.lifetime_work_cycles}) ({current_config['name']})"
        elif ws_target.has_started and ws_target.running:
            ghosty_state = f"🚀 Working (Cycle #{ws_target.lifetime_work_cycles + 1}) ({current_config['name']})"
        else:
            ghosty_state = f"⚫ Not Running ({current_config['name']})"
    else:
        if ws_target.sleep_mode:
            ghosty_state = f"😴 Sleeping ({current_config['name']})"
            if ws_target.sleep_start_time:
                sleep_elapsed = datetime.now() - ws_target.sleep_start_time
                hrs, rem = divmod(int(sleep_elapsed.total_seconds()), 3600)
                mins, secs = divmod(rem, 60)
                ghosty_state += f" | Slept: {hrs}h {mins}m {secs}s"
        elif ws_target.has_started and ws_target.running:
            ghosty_state = f"🟢 Running ({current_config['name']})"
        else:
            ghosty_state = f"⚫ Not Running ({current_config['name']})"

    ghosty_uptime = datetime.now() - ws_target.ghosty_start_time
    hrs, rem = divmod(int(ghosty_uptime.total_seconds()), 3600)
    mins, secs = divmod(rem, 60)

    profit_text = ""
    if live_fetch and ws_target.has_started and ws_target.zoo_channel and not ws_target.sleep_mode and not ws_target.paused:
        await ctx.send("🔍 Fetching current zoo data for profit calculation...")
        await ws_target.zoo_channel.send("owo zoo")
        await made_by_ghosty.sleep(5)
        try:
            messages = [msg async for msg in ws_target.zoo_channel.history(limit=10)]
            zoo_messages = []
            for msg in messages:
                if msg.author.id == 408785106942164992:
                    content_lower = msg.content.lower()
                    if (any(kw in content_lower for kw in ["zoo", "animals", "cowoncy", "points:"]) or any(sup in msg.content for sup in "⁰¹²³⁴⁵⁶⁷⁸⁹")):
                        zoo_messages.append(msg.content)
                        if "common" in content_lower:
                            break
            if zoo_messages:
                zoo_messages.reverse()
                zoo_data = await parse_zoo_message(zoo_messages)
                ws_target.current_cash = zoo_data["total_cash"]
                ws_target.current_essence = zoo_data["total_essence"]
                cash_profit = ws_target.current_cash - ws_target.initial_cash
                essence_profit = ws_target.current_essence - ws_target.initial_essence
                profit_text = (
                    f"\n\n💰 **Profit Since Start:**\n"
                    f"> 💵 Cash: {format_value(cash_profit)} ({format_value(ws_target.initial_cash)} → {format_value(ws_target.current_cash)})\n"
                    f"> ✨ Essence: {format_value(essence_profit)} ({format_value(ws_target.initial_essence)} → {format_value(ws_target.current_essence)})"
                )
        except Exception as e:
            log_worker_event(ws_target.worker_number, f"Error fetching status zoo data: {e}", "WARNING")
            profit_text = "\n\n⚠ Could not fetch current zoo data."
    elif not live_fetch and ws_target.has_started:
        if ws_target.current_cash or ws_target.current_essence:
            cash_profit = ws_target.current_cash - ws_target.initial_cash
            essence_profit = ws_target.current_essence - ws_target.initial_essence
            profit_text = (
                f"\n\n💰 **Profit (Cached):**\n"
                f"> 💵 Cash: {format_value(cash_profit)} ({format_value(ws_target.initial_cash)} → {format_value(ws_target.current_cash)})\n"
                f"> ✨ Essence: {format_value(essence_profit)} ({format_value(ws_target.initial_essence)} → {format_value(ws_target.current_essence)})"
            )

    lifetime_info = ""
    if ws_target.current_speed_mode == "lifetime":
        lifetime_info = (
            f"\n> ♾️ **Work Cycles:** {ws_target.lifetime_work_cycles}\n"
            f"> 🌙 **Day Skip Active:** {'Yes' if ws_target.lifetime_day_skip_active else 'No'}"
        )
        if ws_target.lifetime_cycle_start_time:
            cycle_elapsed = datetime.now() - ws_target.lifetime_cycle_start_time
            cycle_hrs, cycle_rem = divmod(int(cycle_elapsed.total_seconds()), 3600)
            cycle_mins = cycle_rem // 60
            lifetime_info += f"\n> ⏱️ **Current Cycle Duration:** {cycle_hrs}h {cycle_mins}m"

    if not ws_target.huntbot_enabled:
        hb_status = "🔴 Disabled"
    elif ws_target.GhoStyHbAlrActiveVar:
        hb_status = "✅ Active"
    else:
        hb_status = "⏳ Inactive"

    pause_info = ""
    if ws_target.paused and ws_target.pause_end_time:
        pause_info = f"\n> ⏸️ **Paused Until:** {ws_target.pause_end_time.strftime('%d-%b-%Y %I:%M:%S %p')}"

    boss_status = f"{ws_target.boss_tickets}/3 Tickets"
    if ws_target.boss_tickets <= 0:
        boss_status += " 🚫 (Out of Tickets)"
    elif ws_target.is_boss_fighting:
        boss_status += " ⚔️ (Fighting Now!)"
    elif ws_target.next_boss_fight_time:
        boss_status += f" ⏳ (Next Check: <t:{int(ws_target.next_boss_fight_time.timestamp())}:R>)"

    gstatusghosty = f"""
🔍 **GhoSty OwO Worker #{ws_target.worker_number} Status:** {ghosty_state}

> 👤 **Username:** {ws_target.username}
> 🕒 **Running Since:** {ws_target.ghosty_start_time.strftime('%d-%b-%Y %I:%M:%S %p')}
> 📈 **Uptime:** {hrs}h {mins}m {secs}s
> 📊 **Commands Sent:** {ws_target.ghosty_commands_sent}
> 💎 **Gems Potentially Used:** {ws_target.ghosty_gems_used}
> ⚡ **Speed Mode:** {current_config['name']}{lifetime_info}
> 🛏️ **Sleeping?:** {"Yes" if ws_target.sleep_mode else "No"}
> 🎯 **HuntBot:** {hb_status}
> 🧠 **HuntBot Solver:** {"Available" if ws_target.GhoStyCoreAvailCheck else "Not Available"}
> 👹 **Guild Boss:** {boss_status}
> ♻️ **Last Gem Check:** {'<t:' + str(int(ws_target.last_gem_check)) + ':R>' if ws_target.last_gem_check else 'Never'}{pause_info}{profit_text}
"""
    await ctx.send(gstatusghosty)



class PseudoCtx:
    def __init__(self, channel, bot_instance):
        self.channel = channel
        self.bot = bot_instance
        self.author = bot_instance.user

    async def send(self, *args, **kwargs):
        return await self.channel.send(*args, **kwargs)


def _has_main_controller_args(ctx):

    raw = ctx.message.content.strip()

    after = raw[len(ctx.prefix + ctx.invoked_with):].strip()
    if not after:
        return False

    first = after.split()[0].lower().rstrip(",")
    return first == "all" or first.isdigit()


def register_commands(bot, ws):

    @bot.command(aliases=["h"])
    async def help(ctx):
        if ctx.author.id != bot.user.id:
            return
        ghosty_help = """
    # 🤑 GhoSty OwO Farm V4.1 🤑 
Prefix: `.`

**__Main__**
 🌟 `.start` — Start farming in this channel
 🛑 `.stop` — Stop this worker
 🔍 `.status` — Show worker status
 ⚡ `.speed [mode]` — View/change speed mode
 🎯 `.huntbot [on/off]` — Toggle auto-HuntBot
 ⏸️ `.pause <time>` — Pause farming (min 15m, e.g. .pause 30m / .pause 1h)
 ▶️ `.resume` — Resume from pause early

**__Speed Modes__**
 `efficient` | `fast` | `durable` | `lifetime` (default)

**__Made with 💖 and 🧠 by GhoSty | [Async Development]__** 
"""
        await ctx.send(ghosty_help)

    @bot.command()
    async def speed(ctx, mode: str = None):
        if ctx.author.id != bot.user.id:
            return

        if _has_main_controller_args(ctx):
            return

        if mode is None:
            current_config = SPEED_MODES[ws.current_speed_mode]
            await ctx.send(
                f"⚡ Current speed mode: **{current_config['name']}**\n\n"
                "Available modes: `efficient`, `fast`, `durable`, `lifetime`"
            )
            return

        mode = mode.lower()
        if mode not in SPEED_MODES:
            await ctx.send("❌ Invalid speed mode. Available: `efficient`, `fast`, `durable`, `lifetime`, `humanoid`")
            return

        ws.current_speed_mode = mode
        ws.last_mode_change_time = datetime.now()
        current_config = SPEED_MODES[ws.current_speed_mode]
        await ctx.send(f"✅ Speed mode changed to: **{current_config['name']}**")

    @bot.command()
    async def start(ctx):
        if ctx.author.id != bot.user.id:
            return

        if _has_main_controller_args(ctx):
            return

        if ws.running and ws.has_started:
            await ctx.send(
                "⚠️ **GhoSty OwO Worker is already running!**\n\n"
                "🛑 Please use `.stop` first, then `.start` to restart."
            )
            return

        success, blocking_worker = manager.try_claim_channel(ctx.channel.id, ws.worker_number)
        if not success:
            bw = manager.get_worker(blocking_worker)
            bw_name = bw.username if bw else "Unknown"
            await ctx.send(
                f"GhoSty OwO Worker number {blocking_worker} with username {bw_name} already working in this channel."
            )
            return

        await ctx.send(f"🌟 **GhoSty OwO Worker #{ws.worker_number} Starting!**")
        await _run_farming_loop(ctx, ws, bot)

    @bot.command()
    async def stop(ctx):
        if ctx.author.id != bot.user.id:
            return

        if _has_main_controller_args(ctx):
            return

        await ctx.send("🛑 Stopping | Type `.start` again to re-start grinding")
        ws.running = False
        ws.has_started = False
        ws.sleep_mode = False
        ws.paused = False
        ws.pause_end_time = None
        manager.release_channel(ctx.channel.id, ws.worker_number)

    @bot.command()
    async def status(ctx):
        if ctx.author.id != bot.user.id:
            return
        if _has_main_controller_args(ctx):
            return

        await _send_status(ctx, ws, live_fetch=True)

    @bot.command()
    async def mail(ctx):
        if ctx.author.id != bot.user.id:
            return

        if _has_main_controller_args(ctx):
            return

        if ws.last_mail_claim:
            time_since = (datetime.now() - ws.last_mail_claim).total_seconds()
            if time_since < 300:
                await ctx.send(f"⏳ **Cooldown active!** Please wait {int(300 - time_since)}s before checking mail again.")
                return

        if ws.is_mail_claiming:
            await ctx.send("⚠️ Currently already checking mail. Please wait.")
            return

        ws.last_mail_claim = datetime.now()
        ws.is_mail_claiming = True
        await ctx.send("📩 Started checking mailbox in the background...")
        from core.mailmodule import execute_mail_claim
        bot.loop.create_task(execute_mail_claim(ctx, ws, bot))

    @bot.command()
    async def huntbot(ctx, toggle: str = None):
        if ctx.author.id != bot.user.id:
            return

        if _has_main_controller_args(ctx):
            return

        if toggle is None:
            state = "🟢 ON" if ws.huntbot_enabled else "🔴 OFF"
            await ctx.send(f"🎯 **Auto-HuntBot is currently: {state}**\nUse `.huntbot on` or `.huntbot off` to toggle.")
            return

        toggle = toggle.lower()
        if toggle == "on":
            ws.huntbot_enabled = True
            await ctx.send("✅ **Auto-HuntBot is now ON.** Will trigger on next `.start`.")
        elif toggle == "off":
            if ws.GhoStyHbAlrActiveVar:
                ws.GhoStyHbAlrActiveVar = False
                log_worker_event(ws.worker_number, "HuntBot toggled off while active — resetting tracking", "INFO")
            ws.huntbot_enabled = False
            await ctx.send("🔴 **Auto-HuntBot is now OFF.** HuntBot will be skipped.")
        else:
            await ctx.send("❌ Invalid option. Use `.huntbot on` or `.huntbot off`")

    @bot.command()
    async def pause(ctx, time_str: str = None):
        if ctx.author.id != bot.user.id:
            return

        if _has_main_controller_args(ctx):
            return

        if time_str is None:
            if ws.paused and ws.pause_end_time:
                remaining = ws.pause_end_time - datetime.now()
                rem_secs = max(0, int(remaining.total_seconds()))
                await ctx.send(
                    f"⏸️ **Currently paused.** Resumes at "
                    f"**{ws.pause_end_time.strftime('%d-%b-%Y %I:%M:%S %p')}** "
                    f"({_format_duration(rem_secs)} remaining)\n"
                    f"Use `.resume` to end the pause early."
                )
            else:
                await ctx.send(
                    "❌ No active pause. Usage: `.pause 30m` / `.pause 1h` / `.pause 1h30m`\n"
                    "Minimum pause time is **15 minutes**."
                )
            return

        if not ws.running or not ws.has_started:
            await ctx.send("❌ Worker is not running. Use `.start` first.")
            return

        if ws.paused:
            await ctx.send(
                f"⏸️ Already paused until **{ws.pause_end_time.strftime('%d-%b-%Y %I:%M:%S %p')}**.\n"
                f"Use `.resume` to end the pause early."
            )
            return

        secs = _parse_pause_time(time_str)
        if secs is None:
            await ctx.send("❌ Invalid time format. Examples: `.pause 30m` / `.pause 1h` / `.pause 1h30m`")
            return

        if secs < 900:
            await ctx.send("❌ Minimum pause time is **15 minutes**. Example: `.pause 15m`")
            return

        ws.paused = True
        ws.pause_end_time = datetime.now() + timedelta(seconds=secs)
        resume_str = ws.pause_end_time.strftime('%d-%b-%Y %I:%M:%S %p')

        extra = ""
        if ws.sleep_mode or ws.lifetime_day_skip_active:
            extra = "\n⚠️ A natural sleep is currently running — pause will begin after it completes."
        if secs > 86400:
            extra += f"\n⚠️ Long pause ({_format_duration(secs)}) — use `.stop` if you meant to stop entirely."

        await ctx.send(
            f"⏸️ **Farming paused for {_format_duration(secs)}.**\n"
            f"Auto-resumes at **{resume_str}**{extra}"
        )
        log_worker_event(ws.worker_number, f"⏸️ Paused for {_format_duration(secs)}", "INFO")

    @bot.command()
    async def resume(ctx):
        if ctx.author.id != bot.user.id:
            return

        if _has_main_controller_args(ctx):
            return

        if not ws.paused:
            await ctx.send("❌ Worker is not currently paused.")
            return

        ws.paused = False
        ws.pause_end_time = None
        ws.farming_start_time = datetime.now()
        ws.last_mode_change_time = datetime.now()
        if ws.lifetime_cycle_start_time is not None:
            ws.lifetime_cycle_start_time = datetime.now()
        await ctx.send("▶️ **Pause cancelled. Resuming farming on next cycle.**")
        log_worker_event(ws.worker_number, "▶️ Manual resume from pause", "INFO")

    ws.bot = bot

def register_main_commands(bot):

    @bot.command()
    async def help(ctx):
        if ctx.author.id != bot.user.id:
            return
        main_help = f"""
# 🎮 GhoSty OwO Main Controller

Prefix: `.`   **Total Workers:** {manager.total_workers}

**__Worker Management__**
 📋 `.workers` — List all workers and their status
 🌟 `.start <N/N,M>` — Start specific worker(s) in this channel
 🌟 `.start all` — Start all workers using channels.txt pairing
 🛑 `.stop <N/N,M/all>` — Stop specific/all workers
 🔍 `.status <N>` — Show a specific worker's status
 💰 `.profit` — Show cash profit summary across all workers
 💬 `.say <text>` — Make all workers send text in their designated channels

**__Control__**
 ⚡ `.speed <N/all> <mode>` — Change speed mode for worker(s)
 🎯 `.huntbot <N/all> <on/off>` — Toggle auto-HuntBot
 ⏸️ `.pause <N/all> <time>` — Pause worker(s) (e.g. .pause 1 30m)
 ▶️ `.resume <N/all>` — Resume paused worker(s)

**__Speed Modes:__** `efficient` | `fast` | `durable` | `lifetime` | `humanoid`
**__Made with 💖 by GhoSty | [Async Development]__**
"""
        await ctx.send(main_help)

    @bot.command()
    async def workers(ctx):
        if ctx.author.id != bot.user.id:
            return

        all_ws = manager.get_all_workers()
        if not all_ws:
            await ctx.send("⚫ No workers registered yet.")
            return

        lines = [f"📋 **GhoSty OwO Workers ({manager.total_workers} total):**\n"]
        for wn, w in sorted(all_ws.items()):
            if w.paused:
                icon = "⏸️"
            elif w.running and w.has_started and not w.sleep_mode:
                icon = "🟢"
            elif w.sleep_mode:
                icon = "😴"
            else:
                icon = "⚫"
            hb = "🎯" if w.huntbot_enabled else "🔴"
            lines.append(f"> {icon} Worker #{wn} — {w.username} {hb}")
        await ctx.send("\n".join(lines))

    @bot.command()
    async def start(ctx, *, args: str = None):
        if ctx.author.id != bot.user.id:
            return

        if args is None:
            await ctx.send(
                "❌ Usage: `.start <N>` / `.start 1, 2, 3` / `.start all`\n"
                "Note: `.start all` requires channels.txt to be configured."
            )
            return

        use_all = args.strip().lower() == "all"

        if use_all:
            if not manager.has_channels_config:
                await ctx.send(
                    "❌ **No channels configured.** Add channel IDs to `channels.txt` to use `.start all`."
                )
                return

            started_count = 0
            skipped = []
            for wn, target_ws in sorted(manager.get_all_workers().items()):
                ch_id = target_ws.auto_start_channel_id
                if ch_id is None:
                    skipped.append(f"Worker #{wn}: no channel assigned in channels.txt")
                    continue

                if target_ws.running and target_ws.has_started:
                    skipped.append(f"Worker #{wn} ({target_ws.username}): already running")
                    continue

                success, blocking = manager.try_claim_channel(ch_id, wn)
                if not success:
                    bw = manager.get_worker(blocking)
                    bw_name = bw.username if bw else "Unknown"
                    skipped.append(
                        f"Worker #{wn}: channel locked by Worker #{blocking} ({bw_name})"
                    )
                    continue

                target_bot = target_ws.bot
                if not (target_bot and target_bot.loop and target_bot.loop.is_running()):
                    manager.release_channel(ch_id, wn)
                    skipped.append(f"Worker #{wn}: bot not connected yet")
                    continue

                target_channel = target_bot.get_channel(ch_id)
                if not target_channel:
                    manager.release_channel(ch_id, wn)
                    skipped.append(f"Worker #{wn}: cannot see channel {ch_id} (not in server?)")
                    continue

                pseudo_ctx = PseudoCtx(target_channel, target_bot)
                made_by_ghosty.run_coroutine_threadsafe(
                    _run_farming_loop(pseudo_ctx, target_ws, target_bot),
                    target_bot.loop,
                )
                started_count += 1

            reply_lines = [f"🌟 **Started {started_count} worker(s) via channels.txt.**"]
            if skipped:
                reply_lines.append("\n⚠️ **Skipped:**")
                for s in skipped:
                    reply_lines.append(f"> {s}")
            await ctx.send("\n".join(reply_lines))
            return

        target_numbers = _parse_worker_args(args)
        if target_numbers is None:
            await ctx.send(f"❌ Invalid worker number in: `{args}`")
            return
        if not target_numbers:
            await ctx.send("❌ No valid worker numbers provided.")
            return

        for wn in target_numbers:
            target_ws = manager.get_worker(wn)
            if target_ws is None:
                await ctx.send(f"❌ Worker {wn} does not exist. Available: 1-{manager.total_workers}")
                continue

            if target_ws.running and target_ws.has_started:
                await ctx.send(
                    f"⚠️ Worker #{wn} ({target_ws.username}) is already running! Use `.stop {wn}` first."
                )
                continue

            success, blocking = manager.try_claim_channel(ctx.channel.id, wn)
            if not success:
                bw = manager.get_worker(blocking)
                bw_name = bw.username if bw else "Unknown"
                await ctx.send(
                    f"GhoSty OwO Worker number {blocking} with username {bw_name} already working in this channel."
                )
                continue

            target_bot = target_ws.bot
            if not (target_bot and target_bot.loop and target_bot.loop.is_running()):
                manager.release_channel(ctx.channel.id, wn)
                await ctx.send(f"⚠️ Worker #{wn} bot is not connected yet. Try again shortly.")
                continue

            target_channel = target_bot.get_channel(ctx.channel.id)
            if not target_channel:
                manager.release_channel(ctx.channel.id, wn)
                await ctx.send(f"⚠️ Worker #{wn} cannot see this channel.")
                continue

            await ctx.send(f"🌟 Starting Worker #{wn} ({target_ws.username}) in this channel...")
            pseudo_ctx = PseudoCtx(target_channel, target_bot)
            made_by_ghosty.run_coroutine_threadsafe(
                _run_farming_loop(pseudo_ctx, target_ws, target_bot),
                target_bot.loop,
            )

    @bot.command()
    async def stop(ctx, *, args: str = None):
        if ctx.author.id != bot.user.id:
            return

        if args is None:
            await ctx.send(
                "❌ Usage: `.stop <N>` / `.stop 1, 2, 3` / `.stop all`"
            )
            return

        target_numbers = _parse_worker_args(args)
        if target_numbers is None:
            await ctx.send(f"❌ Invalid worker number in: `{args}`")
            return

        for wn in target_numbers:
            target_ws = manager.get_worker(wn)
            if target_ws is None:
                await ctx.send(f"❌ Worker {wn} does not exist. Available: 1-{manager.total_workers}")
                continue

            if not target_ws.running and not target_ws.has_started:
                await ctx.send(f"⚫ Worker #{wn} ({target_ws.username}) is not running.")
                continue

            target_ws.running = False
            target_ws.has_started = False
            target_ws.sleep_mode = False
            target_ws.paused = False
            target_ws.pause_end_time = None
            if target_ws.active_channel_id:
                manager.release_channel(target_ws.active_channel_id, wn)
            await ctx.send(f"🛑 Worker #{wn} ({target_ws.username}) stopped.")

    @bot.command()
    async def status(ctx, worker_number: int = None):
        if ctx.author.id != bot.user.id:
            return

        if worker_number is None:
            await ctx.send(
                "❌ Usage: `.status <worker_number>`\n"
                "Example: `.status 1`\n"
                "Use `.workers` to see all workers at a glance."
            )
            return

        target_ws = manager.get_worker(worker_number)
        if target_ws is None:
            await ctx.send(f"❌ Worker {worker_number} does not exist. Available: 1-{manager.total_workers}")
            return

        if (
            target_ws.has_started
            and target_ws.zoo_channel
            and not target_ws.sleep_mode
            and not target_ws.paused
            and target_ws.bot
            and target_ws.bot.loop
            and target_ws.bot.loop.is_running()
        ):
            try:
                await ctx.send("🔍 Fetching live zoo data for Worker #{}...".format(worker_number))
                future = made_by_ghosty.run_coroutine_threadsafe(
                    _fetch_zoo_for_main_status(target_ws),
                    target_ws.bot.loop,
                )
                await made_by_ghosty.wrap_future(future)
            except Exception as e:
                log_worker_event("CTRL", f"Zoo fetch failed for W#{worker_number}: {e}", "WARNING")

        await _send_status(ctx, target_ws, live_fetch=False)

    @bot.command()
    async def speed(ctx, *, args: str = None):
        if ctx.author.id != bot.user.id:
            return

        if args is None:
            await ctx.send(
                "❌ Usage: `.speed <N/all> <mode>`\n"
                "Example: `.speed 1 lifetime` / `.speed all durable`\n"
                "Modes: `efficient`, `fast`, `durable`, `lifetime`"
            )
            return

        parts = args.split()
        if len(parts) < 2:
            await ctx.send(
                "❌ Usage: `.speed <N/all> <mode>`\n"
                "Example: `.speed 1 lifetime` / `.speed all durable`"
            )
            return

        mode = parts[-1].lower()
        if mode not in SPEED_MODES:
            await ctx.send(f"❌ Unknown speed mode `{mode}`. Available: `efficient`, `fast`, `durable`, `lifetime`, `humanoid`")
            return

        worker_spec = " ".join(parts[:-1])
        target_numbers = _parse_worker_args(worker_spec)
        if target_numbers is None:
            await ctx.send(f"❌ Invalid worker number in: `{worker_spec}`")
            return
        if not target_numbers:
            await ctx.send("❌ No valid worker numbers provided.")
            return

        current_config = SPEED_MODES[mode]
        changed = []
        for wn in target_numbers:
            target_ws = manager.get_worker(wn)
            if target_ws is None:
                await ctx.send(f"❌ Worker {wn} does not exist.")
                continue
            target_ws.current_speed_mode = mode
            target_ws.last_mode_change_time = datetime.now()
            changed.append(f"Worker #{wn} ({target_ws.username})")

        if changed:
            await ctx.send(
                f"✅ Speed mode set to **{current_config['name']}** for: "
                + ", ".join(changed)
            )

    @bot.command()
    async def huntbot(ctx, *, args: str = None):
        if ctx.author.id != bot.user.id:
            return

        if args is None:
            await ctx.send(
                "❌ Usage: `.huntbot <N/all> <on/off>`\n"
                "Example: `.huntbot 1 off` / `.huntbot all on`"
            )
            return

        parts = args.split()
        if len(parts) < 2:
            await ctx.send("❌ Usage: `.huntbot <N/all> <on/off>`")
            return

        toggle = parts[-1].lower()
        if toggle not in ("on", "off"):
            await ctx.send("❌ Toggle must be `on` or `off`. Example: `.huntbot all off`")
            return

        worker_spec = " ".join(parts[:-1])
        target_numbers = _parse_worker_args(worker_spec)
        if target_numbers is None:
            await ctx.send(f"❌ Invalid worker number in: `{worker_spec}`")
            return
        if not target_numbers:
            await ctx.send("❌ No valid worker numbers provided.")
            return

        changed = []
        for wn in target_numbers:
            target_ws = manager.get_worker(wn)
            if target_ws is None:
                await ctx.send(f"❌ Worker {wn} does not exist.")
                continue
            if toggle == "on":
                target_ws.huntbot_enabled = True
            else:
                if target_ws.GhoStyHbAlrActiveVar:
                    target_ws.GhoStyHbAlrActiveVar = False
                target_ws.huntbot_enabled = False
            changed.append(f"Worker #{wn} ({target_ws.username})")

        state_str = "🟢 ON" if toggle == "on" else "🔴 OFF"
        if changed:
            await ctx.send(
                f"🎯 Auto-HuntBot set to **{state_str}** for: " + ", ".join(changed)
            )

    @bot.command()
    async def pause(ctx, *, args: str = None):
        if ctx.author.id != bot.user.id:
            return

        if args is None:
            await ctx.send(
                "❌ Usage: `.pause <N/all> <time>`\n"
                "Example: `.pause 1 30m` / `.pause all 1h` / `.pause 2, 3 1h30m`\n"
                "Minimum pause time is **15 minutes**."
            )
            return

        parts = args.split()
        if len(parts) < 2:
            await ctx.send(
                "❌ Usage: `.pause <N/all> <time>`\n"
                "Example: `.pause 1 30m` / `.pause all 1h`"
            )
            return

        time_str = parts[-1].lower()
        worker_spec = " ".join(parts[:-1])

        secs = _parse_pause_time(time_str)
        if secs is None:
            await ctx.send("❌ Invalid time format. Examples: `30m`, `1h`, `1h30m`")
            return

        if secs < 900:
            await ctx.send("❌ Minimum pause time is **15 minutes**. Example: `.pause all 15m`")
            return

        target_numbers = _parse_worker_args(worker_spec)
        if target_numbers is None:
            await ctx.send(f"❌ Invalid worker number in: `{worker_spec}`")
            return
        if not target_numbers:
            await ctx.send("❌ No valid worker numbers provided.")
            return

        pause_end = datetime.now() + timedelta(seconds=secs)
        applied = []
        skipped = []

        for wn in target_numbers:
            target_ws = manager.get_worker(wn)
            if target_ws is None:
                skipped.append(f"Worker #{wn}: does not exist")
                continue
            if not target_ws.running or not target_ws.has_started:
                skipped.append(f"Worker #{wn} ({target_ws.username}): not running")
                continue
            if target_ws.paused:
                skipped.append(
                    f"Worker #{wn} ({target_ws.username}): already paused until "
                    f"{target_ws.pause_end_time.strftime('%H:%M:%S')}"
                )
                continue
            target_ws.paused = True
            target_ws.pause_end_time = pause_end
            applied.append(f"Worker #{wn} ({target_ws.username})")
            log_worker_event(wn, f"⏸️ Paused via main controller for {_format_duration(secs)}", "INFO")

        lines = []
        if applied:
            extra = ""
            if secs > 86400:
                extra = f" ⚠️ Long pause ({_format_duration(secs)})."
            lines.append(
                f"⏸️ **Paused for {_format_duration(secs)}** — auto-resumes at "
                f"**{pause_end.strftime('%d-%b-%Y %I:%M:%S %p')}**{extra}\n"
                f"Applied to: " + ", ".join(applied)
            )
        if skipped:
            lines.append("\n⚠️ **Skipped:**\n" + "\n".join(f"> {s}" for s in skipped))
        if lines:
            await ctx.send("\n".join(lines))

    @bot.command()
    async def resume(ctx, *, args: str = None):
        if ctx.author.id != bot.user.id:
            return

        if args is None:
            await ctx.send(
                "❌ Usage: `.resume <N/all>`\n"
                "Example: `.resume 1` / `.resume all`"
            )
            return

        target_numbers = _parse_worker_args(args)
        if target_numbers is None:
            await ctx.send(f"❌ Invalid worker number in: `{args}`")
            return
        if not target_numbers:
            await ctx.send("❌ No valid worker numbers provided.")
            return

        resumed = []
        skipped = []

        for wn in target_numbers:
            target_ws = manager.get_worker(wn)
            if target_ws is None:
                skipped.append(f"Worker #{wn}: does not exist")
                continue
            if not target_ws.paused:
                skipped.append(f"Worker #{wn} ({target_ws.username}): not paused")
                continue
            target_ws.paused = False
            target_ws.pause_end_time = None
            target_ws.farming_start_time = datetime.now()
            target_ws.last_mode_change_time = datetime.now()
            if target_ws.lifetime_cycle_start_time is not None:
                target_ws.lifetime_cycle_start_time = datetime.now()
            resumed.append(f"Worker #{wn} ({target_ws.username})")
            log_worker_event(wn, "▶️ Resumed via main controller", "INFO")

        lines = []
        if resumed:
            lines.append("▶️ **Resumed:** " + ", ".join(resumed))
        if skipped:
            lines.append("⚠️ **Skipped:** " + " | ".join(skipped))
        if lines:
            await ctx.send("\n".join(lines))

    @bot.command()
    async def profit(ctx):
        if ctx.author.id != bot.user.id:
            return

        all_ws = manager.get_all_workers()
        if not all_ws:
            await ctx.send("⚫ No workers registered.")
            return

        await ctx.send("💰 Fetching live zoo data for all active workers...")

        for wn, target_ws in sorted(all_ws.items()):
            if (
                target_ws.has_started
                and target_ws.zoo_channel
                and not target_ws.sleep_mode
                and not target_ws.paused
                and target_ws.bot
                and target_ws.bot.loop
                and target_ws.bot.loop.is_running()
            ):
                try:
                    future = made_by_ghosty.run_coroutine_threadsafe(
                        _fetch_zoo_for_main_status(target_ws),
                        target_ws.bot.loop,
                    )
                    await made_by_ghosty.wrap_future(future)
                except Exception as e:
                    log_worker_event("CTRL", f"Profit zoo fetch failed for W#{wn}: {e}", "WARNING")

        lines = ["💰 **GhoSty OwO Profit Summary:**\n"]
        total_profit = 0

        for wn, target_ws in sorted(all_ws.items()):
            if not target_ws.has_started:
                lines.append(f"> Worker {wn} ({target_ws.username}): ⚫ Not started")
                continue

            profit = target_ws.current_cash - target_ws.initial_cash
            total_profit += profit

            if target_ws.sleep_mode:
                state_tag = " 😴"
            elif target_ws.paused:
                state_tag = " ⏸️"
            elif not target_ws.running:
                state_tag = " 🛑"
            else:
                state_tag = ""

            profit_sign = "+" if profit >= 0 else ""
            lines.append(
                f"> Worker {wn} ({target_ws.username}){state_tag}: "
                f"**{profit_sign}{format_value(profit)}** "
                f"({format_value(target_ws.initial_cash)} → {format_value(target_ws.current_cash)})"
            )

        total_sign = "+" if total_profit >= 0 else ""
        lines.append(
            f"\n> 💵 **Total Cash Profit Across All Workers: {total_sign}{format_value(total_profit)}**"
        )

        await ctx.send("\n".join(lines))

    @bot.command()
    async def say(ctx, *, text: str = None):
        if ctx.author.id != bot.user.id:
            return

        if text is None or not text.strip():
            await ctx.send(
                "❌ Usage: `.say <text>`\n"
                "Example: `.say Hello everyone!`\n"
                "Makes all workers send the text in their designated channels."
            )
            return

        text = text.strip()
        all_ws = manager.get_all_workers()
        if not all_ws:
            await ctx.send("⚫ No workers registered.")
            return

        sent = []
        skipped = []

        for wn, target_ws in sorted(all_ws.items()):
            ch_id = target_ws.auto_start_channel_id

            if ch_id is None:
                skipped.append(f"Worker #{wn} ({target_ws.username}): no channel assigned in channels.txt")
                continue

            target_bot = target_ws.bot
            if not (target_bot and target_bot.loop and target_bot.loop.is_running()):
                skipped.append(f"Worker #{wn} ({target_ws.username}): bot not connected")
                continue

            channel = target_bot.get_channel(ch_id)
            if not channel:
                skipped.append(f"Worker #{wn} ({target_ws.username}): cannot see channel {ch_id}")
                continue

            try:
                made_by_ghosty.run_coroutine_threadsafe(
                    channel.send(text),
                    target_bot.loop,
                )
                sent.append(f"Worker #{wn} ({target_ws.username})")
                log_worker_event(wn, f".say dispatched to channel {ch_id}", "INFO")
            except Exception as e:
                skipped.append(f"Worker #{wn} ({target_ws.username}): send error — {e}")
                log_worker_event(wn, f".say error: {e}", "WARNING")

        reply_lines = []
        if sent:
            reply_lines.append(f"💬 **Sent to {len(sent)} worker channel(s):** " + ", ".join(sent))
        if skipped:
            reply_lines.append("⚠️ **Skipped:**\n" + "\n".join(f"> {s}" for s in skipped))
        if not sent and not skipped:
            reply_lines.append("⚫ No workers had designated channels to send to.")

        await ctx.send("\n".join(reply_lines))

    @bot.command()
    async def mail(ctx, *, args: str = None):
        if ctx.author.id != bot.user.id:
            return

        if args is None:
            await ctx.send("❌ Usage: `.mail all` or `.mail 1, 2`")
            return

        target_numbers = _parse_worker_args(args)
        if target_numbers is None:
            await ctx.send(f"❌ Invalid worker number in: `{args}`")
            return
        if not target_numbers:
            await ctx.send("❌ No valid worker numbers provided.")
            return

        started = []
        skipped = []

        for wn in target_numbers:
            target_ws = manager.get_worker(wn)
            if target_ws is None:
                skipped.append(f"Worker #{wn}: does not exist")
                continue
            
            target_bot = target_ws.bot
            if not (target_bot and target_bot.loop and target_bot.loop.is_running()):
                skipped.append(f"Worker #{wn} ({target_ws.username}): bot not connected")
                continue
                
            ch_id = target_ws.auto_start_channel_id
            if ch_id is None:
                skipped.append(f"Worker #{wn} ({target_ws.username}): no channel assigned in channels.txt")
                continue
                
            target_channel = target_bot.get_channel(ch_id)
            if not target_channel:
                skipped.append(f"Worker #{wn} ({target_ws.username}): cannot see channel {ch_id}")
                continue

            if target_ws.last_mail_claim:
                time_since = (datetime.now() - target_ws.last_mail_claim).total_seconds()
                if time_since < 300:
                    skipped.append(f"Worker #{wn} ({target_ws.username}): Cooldown active ({int(300 - time_since)}s remaining)")
                    continue

            if getattr(target_ws, "is_mail_claiming", False):
                skipped.append(f"Worker #{wn} ({target_ws.username}): already checking mail")
                continue

            target_ws.last_mail_claim = datetime.now()
            target_ws.is_mail_claiming = True
            started.append(f"Worker #{wn} ({target_ws.username})")
            log_worker_event(wn, ".mail dispatched via main controller", "INFO")
            
            pseudo_ctx = PseudoCtx(target_channel, target_bot)
            from core.mailmodule import execute_mail_claim
            target_bot.loop.create_task(execute_mail_claim(pseudo_ctx, target_ws, target_bot))

        reply_lines = []
        if started:
            reply_lines.append("📩 **Started checking mail for:** " + ", ".join(started))
        if skipped:
            reply_lines.append("⚠️ **Skipped:**\n" + "\n".join(f"> {s}" for s in skipped))

        await ctx.send("\n".join(reply_lines))


def _parse_worker_args(args_str):
    raw = args_str.replace(",", " ").split()

    if "all" in [r.lower() for r in raw]:
        return list(manager.get_all_workers().keys())

    target_numbers = []
    for r in raw:
        r = r.strip()
        if not r:
            continue
        try:
            target_numbers.append(int(r))
        except ValueError:
            return None

    return target_numbers''',
    'core/mailmodule.py': r'''"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty OwO V4 Alpha Build
Stable Alpha Build Version: 280826.4.1.0

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

import asyncio
from datetime import datetime
import discord
from discord.interactions import _wrapped_interaction
from discord.utils import _generate_nonce
from discord.enums import InteractionType
from core.modules import made_by_ghosty, log_worker_event, SPEED_MODES

async def execute_mail_claim(ctx, ws, bot):
    log_worker_event(ws.worker_number, "📩 Checking mailbox...", "INFO")
    
    try:
        await ctx.send("owo mail")
    except Exception as e:
        log_worker_event(ws.worker_number, f"⚠️ Failed to send 'owo mail': {e}", "WARNING")
        ws.is_mail_claiming = False
        return

    owo_bot_id = 408785106942164992

    try:
        mail_msg = None
        worker_username = bot.user.name.lower()
        worker_display = bot.user.display_name.lower()
        worker_id_str = str(bot.user.id)
        
        for _ in range(5):
            await made_by_ghosty.sleep(2.5)
            async for m in ctx.channel.history(limit=25):
                if m.author.id == owo_bot_id:
                    msg_content = m.content.lower()
                    
                    raw_data = {}
                    try:
                        route = discord.http.Route("GET", "/channels/{channel_id}/messages?limit=1&around={message_id}", channel_id=ctx.channel.id, message_id=m.id)
                        req_data = await bot.http.request(route)
                        if isinstance(req_data, list) and len(req_data) > 0:
                            raw_data = req_data[0]
                    except Exception:
                        pass
                        
                    raw_str = str(raw_data).lower()
                    
                    is_for_me = (worker_id_str in msg_content or worker_username in msg_content or worker_display in msg_content or 
                                 worker_id_str in raw_str or worker_username in raw_str or worker_display in raw_str)
                                 
                    if not is_for_me:
                        continue
                        
                    if "you do not have any mail" in msg_content or "you do not have any mail" in raw_str:
                        log_worker_event(ws.worker_number, "🚫 No mail found.", "INFO")
                        ws.is_mail_claiming = False
                        return
                        
                    if 'components' in raw_data and len(raw_data['components']) > 0:
                        if '1465989917103357962' in raw_str or 'closed_mail' in raw_str or '1465989938796433570' in raw_str or 'opened_mail' in raw_str or 'mailbox' in raw_str:
                            mail_msg = m
                            break
                            
            if mail_msg:
                break
                
        if not mail_msg:
            log_worker_event(ws.worker_number, "⚠️ Could not find 'owo mail' response.", "WARNING")
            ws.is_mail_claiming = False
            return
            
    except Exception as e:
        log_worker_event(ws.worker_number, f"⚠️ Error waiting for 'owo mail' response: {e}", "WARNING")
        ws.is_mail_claiming = False
        return

    def find_button_in_components(components_list, check_func, include_disabled=False):
        def _search(data, targets):
            if isinstance(data, dict):
                if data.get('type') == 2 and check_func(data):
                    if include_disabled or not data.get('disabled', False):
                        targets.append(data)
                for v in data.values():
                    _search(v, targets)
            elif isinstance(data, list):
                for item in data:
                    _search(item, targets)
                    
        targets = []
        _search(components_list, targets)
        return targets

    def is_closed_mail(data):
        if data.get('style') == 2:
            return False
            
        emoji = data.get('emoji', {})
        eid = str(emoji.get('id', ''))
        ename = emoji.get('name')
        return eid in ('1465989917103357962', '1465989938796433570') or ename in ('closed_mail', 'opened_mail')

    def is_claim_button(data):
        lbl = str(data.get('label', '')).lower()
        emoji = data.get('emoji', {})
        return 'claim' in lbl or emoji.get('name') == '🎁'

    def is_return_button(data):
        emoji = data.get('emoji', {})
        return str(emoji.get('id', '')) == '1466327293621305385' or emoji.get('name') == 'return'
        
    def is_forward_button(data):
        emoji = data.get('emoji', {})
        return str(emoji.get('id', '')) == '1356883239175717035' or emoji.get('name') == 'forward'
        
    def is_indicator_button(data):
        lbl = str(data.get('label', ''))
        return '/' in lbl

    async def poll_components(expected_state, timeout=12):
        start_time = datetime.now()
        while (datetime.now() - start_time).total_seconds() < timeout:
            try:
                route = discord.http.Route("GET", "/channels/{channel_id}/messages?limit=1&around={message_id}", channel_id=ctx.channel.id, message_id=mail_msg.id)
                raw_data = await bot.http.request(route)
                if isinstance(raw_data, list) and len(raw_data) > 0:
                    raw_data = raw_data[0]
                components = raw_data.get('components', [])
                if expected_state(components):
                    return components
            except Exception:
                pass
            await made_by_ghosty.sleep(1.5)
        return []

    max_mails = 25
    mails_claimed = 0
    
    for _ in range(max_mails):
   
        def check_main_menu(comps):
            return len(find_button_in_components(comps, is_closed_mail)) > 0 or len(find_button_in_components(comps, is_return_button)) == 0

        components = await poll_components(check_main_menu, timeout=12)

        closed_mail_buttons = find_button_in_components(components, is_closed_mail)
        if not closed_mail_buttons:
            
            forward_buttons = find_button_in_components(components, is_forward_button)
            if forward_buttons:
                indicator_buttons = find_button_in_components(components, is_indicator_button, include_disabled=True)
                old_indicator = str(indicator_buttons[0].get('label', '')) if indicator_buttons else ""
                
            
                can_move_forward = True
                if old_indicator and '/' in old_indicator:
                    parts = old_indicator.split('/')
                    if len(parts) == 2 and parts[0].strip() == parts[1].strip():
                        can_move_forward = False
                        
                if can_move_forward:
                    log_worker_event(ws.worker_number, f"➡️ Moving to next mail page (was {old_indicator})...", "DEBUG")
                    try:
                        await _wrapped_interaction(mail_msg._state, _generate_nonce(), InteractionType.component, None, ctx.channel, forward_buttons[0], message=mail_msg)
                    except Exception as e:
                        log_worker_event(ws.worker_number, f"⚠️ Failed to click next page: {e}", "WARNING")
                        break
                        
                   
                    def check_page_changed(comps):
                        ind_btns = find_button_in_components(comps, is_indicator_button, include_disabled=True)
                        if not ind_btns:
                            return False
                        return str(ind_btns[0].get('label', '')) != old_indicator
                        
                    await poll_components(check_page_changed, timeout=12)
                    continue
            
            if mails_claimed > 0:
                log_worker_event(ws.worker_number, f"✅ Claimed {mails_claimed} mails. No more claimable mail found.", "SUCCESS")
            else:
                log_worker_event(ws.worker_number, f"✅ No claimable mail found.", "INFO")
            break

        target_btn = closed_mail_buttons[0]
        log_worker_event(ws.worker_number, "📨 Opening a mail...", "DEBUG")
        
      
        try:
            await _wrapped_interaction(mail_msg._state, _generate_nonce(), InteractionType.component, None, ctx.channel, target_btn, message=mail_msg)
        except Exception as e:
            log_worker_event(ws.worker_number, f"⚠️ Failed to click closed mail: {e}", "WARNING")
            break
            
       
        def check_detail_menu(comps):
            return len(find_button_in_components(comps, is_return_button)) > 0

        components = await poll_components(check_detail_menu, timeout=12)

        
        claim_buttons = find_button_in_components(components, is_claim_button)
        if claim_buttons:
            log_worker_event(ws.worker_number, "🎁 Claiming rewards...", "SUCCESS")
            try:
                await _wrapped_interaction(mail_msg._state, _generate_nonce(), InteractionType.component, None, ctx.channel, claim_buttons[0], message=mail_msg)
                mails_claimed += 1
                await made_by_ghosty.sleep(2)
            except Exception as e:
                log_worker_event(ws.worker_number, f"⚠️ Failed to click claim: {e}", "WARNING")

       
        components = await poll_components(check_detail_menu, timeout=5)

       
        return_buttons = find_button_in_components(components, is_return_button)
        if return_buttons:
            log_worker_event(ws.worker_number, "🔙 Returning to mail list...", "DEBUG")
            try:
                await _wrapped_interaction(mail_msg._state, _generate_nonce(), InteractionType.component, None, ctx.channel, return_buttons[0], message=mail_msg)
            except Exception as e:
                log_worker_event(ws.worker_number, f"⚠️ Failed to click return: {e}", "WARNING")
                break
        else:
            log_worker_event(ws.worker_number, "⚠️ No return button found. Exiting mail loop.", "WARNING")
            break

    ws.is_mail_claiming = False''',
    'core/modules.py': r'''"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty OwO V4 Alpha Build
Stable Alpha Build Version: 280826.4.1.0

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

import re
import asyncio as made_by_ghosty
from .ui import log_worker_event, log_warn

SPEED_MODES = {
    "efficient": {
        "name": "Efficient (Fast)",
        "command_delay": 0.5,
        "action_delay_min": 5.0,
        "action_delay_max": 15.0,
        "random_long_delay_min": 200,
        "random_long_delay_max": 400,
        "gem_check_interval_min": 200,
        "gem_check_interval_max": 290,
        "run_duration_min": 3 * 3600,  
        "run_duration_max": 3.5 * 3600,  
        "sleep_duration_min": 3.5 * 3600,  
        "sleep_duration_max": 4.5 * 3600   
    },
    "fast": {
        "name": "Fast (Very Fast | Not Recommended, Don't Use)",
        "command_delay": 0.3,
        "action_delay_min": 4.5,
        "action_delay_max": 10.0,
        "random_long_delay_min": 160,
        "random_long_delay_max": 200,
        "gem_check_interval_min": 120,
        "gem_check_interval_max": 180,
        "run_duration_min": 1.5 * 3600,  
        "run_duration_max": 2 * 3600,    
        "sleep_duration_min": 3.5 * 3600,  
        "sleep_duration_max": 5 * 3600     
    },
    "durable": {
        "name": "Durable (Safe & Long)",
        "command_delay": 0.35,
        "action_delay_min": 6.5,
        "action_delay_max": 21.0,
        "random_long_delay_min": 300,
        "random_long_delay_max": 600,
        "gem_check_interval_min": 244,
        "gem_check_interval_max": 415,
        "run_duration_min": 5 * 3600,    
        "run_duration_max": 7 * 3600,    
        "sleep_duration_min": 3.5 * 3600,  
        "sleep_duration_max": 5 * 3600   
    },
    "lifetime": {
        "name": "Lifetime (Ultra Long - Detection Bypass)",
        "command_delay": 0.4,
        "action_delay_min": 7.0,
        "action_delay_max": 22.0,
        "random_long_delay_min": 250,
        "random_long_delay_max": 550,
        "gem_check_interval_min": 220,
        "gem_check_interval_max": 380,
        "work_duration_min": 3 * 3600,  
        "work_duration_max": 5 * 3600,  
        "break_duration_min": 10 * 3600,  
        "break_duration_max": 14 * 3600,  
        "day_skip_threshold": 3, 
        "day_skip_duration": 24 * 3600  
    },
    "humanoid": {
        "name": "Humanoid (Experimental)",
        "command_delay": 0.43,
        "action_delay_min": 8.5,
        "action_delay_max": 20.55,
        "random_long_delay_min": 250,
        "random_long_delay_max": 550,
        "gem_check_interval_min": 220,
        "gem_check_interval_max": 380,
        "work_duration_min": 3.78 * 3600,
        "work_duration_max": 6.4 * 3600,
        "break_duration_min": 8 * 3600,
        "break_duration_max": 12 * 3600,
        "day_skip_threshold": 2,
        "day_skip_duration": 24 * 3600
    }
}

def format_value(value):
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    elif value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    elif value >= 1_000:
        return f"{value / 1_000:.2f}K"
    else:
        return str(value)

async def parse_zoo_message(zoo_messages):
    combined_message = "\n".join(zoo_messages)
    
    superscript_map = {
        '⁰': '0', '¹': '1', '²': '2', '³': '3', '⁴': '4',
        '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9'
    }
    
    value_map = {
        "common": {"cash": 1, "essence": 1},
        "uncommon": {"cash": 3, "essence": 5},
        "rare": {"cash": 10, "essence": 20},
        "epic": {"cash": 250, "essence": 250},
        "mythic": {"cash": 5000, "essence": 3000},
        "legendary": {"cash": 15000, "essence": 10000},
        "fabled": {"cash": 250000, "essence": 100000},
        "special": {"cash": 6000, "essence": 5000},
        "hidden": {"cash": 1000000, "essence": 500000},
        "patreon": {"cash": 1000, "essence": 500},
        "cpatreon": {"cash": 50000, "essence": 25000},
        "gem": {"cash": 30000, "essence": 20000},
        "distorted": {"cash": 300000, "essence": 200000},
        "bot": {"cash": 50000, "essence": 10000}
    }
    
    lines = combined_message.split('\n')
    tier_counts = {tier: 0 for tier in value_map}
    current_tier = None
    
    for line in lines:
        tier_match = re.search(r'<a?:(\w+):\d+>', line)
        if tier_match:
            tier_name = tier_match.group(1).lower()
            if tier_name == "botrank":
                tier_name = "bot"
            
            if tier_name in value_map:
                current_tier = tier_name
        
        if current_tier:
            superscript_regex = r'([⁰¹²³⁴⁵⁶⁷⁸⁹]+)'
            for match in re.finditer(superscript_regex, line):
                superscript_str = match.group(1)
                number_str = ''.join(superscript_map.get(char, char) for char in superscript_str)
                if number_str.isdigit():
                    tier_counts[current_tier] += int(number_str)
    
    total_cash = 0
    total_essence = 0
    
    for tier, count in tier_counts.items():
        if count > 0 and tier in value_map:
            total_cash += count * value_map[tier]["cash"]
            total_essence += count * value_map[tier]["essence"]
    
    zoo_points = 0
    zoo_points_patterns = [
        r'Zoo Points?:\s*__?([\d,]+)__?',
        r'Points?:\s*__?([\d,]+)__?',
        r'__?([\d,]+)__?\s*Zoo Points?',
        r'Zoo Points?:\s*([\d,]+)'
    ]
    
    for pattern in zoo_points_patterns:
        match = re.search(pattern, combined_message, re.IGNORECASE)
        if match:
            zoo_points = int(match.group(1).replace(',', ''))
            break
    
    return {
        'total_cash': total_cash,
        'total_essence': total_essence,
        'zoo_points': zoo_points,
        'tier_counts': tier_counts
    }

async def fetch_zoo_data(ctx):
    await ctx.send("owo zoo")
    await made_by_ghosty.sleep(5)
    
    try:
        messages = [msg async for msg in ctx.channel.history(limit=10)]
        zoo_messages = []
        
        for msg in messages:
            if msg.author.id == 408785106942164992:
                content_lower = msg.content.lower()
                if any(kw in content_lower for kw in ['zoo', 'animals', 'cowoncy', 'points:']) or any(sup in msg.content for sup in "⁰¹²³⁴⁵⁶⁷⁸⁹"):
                    zoo_messages.append(msg.content)
                    if "common" in content_lower:
                        break
        
        if zoo_messages:
            zoo_messages.reverse()
            zoo_data = await parse_zoo_message(zoo_messages)
            return zoo_data
        else:
            log_worker_event("ZOO", "No zoo messages found in channel history", "DEBUG")
            return None
            
    except Exception as e:
        log_worker_event("ZOO", f"Error fetching zoo data: {e}", "WARNING")
        return None
    
async def parse_gems(inventory_message):
    rarity_order = ['f', 'l', 'm', 'e', 'r', 'u', 'c']
    gems_by_tier = {
        '1': [],
        '2': [],
        '3': [],
        '4': []
    }
    lines = inventory_message.split('\n')
    for line in lines:
        for tier in ['1', '2', '3', '4']:
            for rarity in rarity_order:
                pattern = fr'`(\d+)`<a?:({rarity}gem{tier}):\d+>'
                match = re.search(pattern, line)
                if match:
                    gem_number = match.group(1)
                    gems_by_tier[tier].append((rarity, gem_number))
    for tier in gems_by_tier:
        gems_by_tier[tier].sort(key=lambda x: rarity_order.index(x[0]))
    selected_gems = []
    for tier in ['1', '2', '3', '4']:
        if gems_by_tier[tier]:
            selected_gems.append(gems_by_tier[tier][0][1])

    return selected_gems''',
    'core/questsmodule.py': r'''"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty OwO V4 Alpha Build
Stable Alpha Build Version: 280826.4.1.0

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

import os
import json
import asyncio
from datetime import datetime, timedelta
import random

from core.ui import log_worker_event
from core.heart import WorkerManager, manager

QUESTS_FILE = "ghostyworkerquests.json"

def LoadGhoStysQuestsData(ws):
    if not os.path.exists(QUESTS_FILE):
        return {}
    try:
        with open(QUESTS_FILE, "r") as f:
            data = json.load(f)
        return data.get(str(ws.worker_number), {})
    except Exception as e:
        log_worker_event(ws.worker_number, f"Failed to load quests data: {e}", "WARNING")
        return {}

def SaveQuestsDataGhoStys(ws, worker_data):
    try:
        data = {}
        if os.path.exists(QUESTS_FILE):
            with open(QUESTS_FILE, "r") as f:
                try:
                    data = json.load(f)
                except:
                    pass
        data[str(ws.worker_number)] = worker_data
        with open(QUESTS_FILE, "w") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        log_worker_event(ws.worker_number, f"Failed to save quests data: {e}", "WARNING")

def extract_text_from_node(node):
    text = ""
    if isinstance(node, dict):
        if "content" in node and isinstance(node["content"], str):
            text += node["content"] + "\n"
        for v in node.values():
            text += extract_text_from_node(v)
    elif isinstance(node, list):
        for item in node:
            text += extract_text_from_node(item)
    return text

def find_button_by_label(data, label, targets):
    if isinstance(data, dict):
        if data.get('type') == 2 and str(data.get('label', '')).lower() == label.lower():
            targets.append(data)
        elif data.get('type') == 2 and 'components' in data:
            pass
        if data.get('type') == 2:
            inner_text = extract_text_from_node(data).lower()
            if label.lower() in inner_text and data not in targets:
                targets.append(data)
                
        for v in data.values():
            find_button_by_label(v, label, targets)
    elif isinstance(data, list):
        for item in data:
            find_button_by_label(item, label, targets)

async def fetch_and_parse_quests(ctx, ws, bot):
    import discord
    from discord.interactions import _wrapped_interaction
    from discord.utils import _generate_nonce
    from discord.enums import InteractionType

    await asyncio.sleep(3.6)
    await ctx.send("owo q")
    await asyncio.sleep(4)

    bs_msg = None
    for _ in range(3):
        messages = [msg async for msg in ctx.channel.history(limit=20)]
        for msg in messages:
            if msg.author.id == 408785106942164992:
                try:
                    route = discord.http.Route("GET", "/channels/{channel_id}/messages?limit=1&around={message_id}", channel_id=ctx.channel.id, message_id=msg.id)
                    raw_data = await bot.http.request(route)
                    if isinstance(raw_data, list) and len(raw_data) > 0:
                        raw_data = raw_data[0]
                    if 'components' in raw_data:
                        raw_str = str(raw_data).lower()
                        if "quest log" in raw_str or "quests" in raw_str:
                            bs_msg = msg
                            break
                except:
                    pass
            if bs_msg:
                break
        if bs_msg:
            break
        await asyncio.sleep(2)
    
    if not bs_msg:
        log_worker_event(ws.worker_number, "Could not find 'owo q' response.", "DEBUG")
        return

    route = discord.http.Route("GET", "/channels/{channel_id}/messages?limit=1&around={message_id}", channel_id=ctx.channel.id, message_id=bs_msg.id)
    raw_data = await bot.http.request(route)
    if isinstance(raw_data, list) and len(raw_data) > 0:
        raw_data = raw_data[0]
        
    raw_str = str(raw_data).lower()
    ws.all_quests_finished = False
    if "you finished all of your quests" in raw_str:
        ws.all_quests_finished = True
        sleep_until = datetime.now() + timedelta(hours=12)
        import re
        match = re.search(r'<t:(\d+)', raw_str)
        if match:
            try:
                timestamp = int(match.group(1))
                sleep_until = datetime.fromtimestamp(timestamp) + timedelta(minutes=1)
            except:
                pass
                
        ws.next_quest_check_time = sleep_until
        log_worker_event(ws.worker_number, f"All quests finished! Sleeping quests until {sleep_until.strftime('%Y-%m-%d %H:%M:%S')}", "SUCCESS")
        active_quests = {}
        SaveQuestsDataGhoStys(ws, active_quests)
        return active_quests
    full_text = extract_text_from_node(raw_data.get('components', []))
    
    active_quests = {}
    lines = full_text.split('\n')
    
    current_quest = None
    for i, line in enumerate(lines):
        line_lower = line.lower()
        if "battle with a friend" in line_lower:
            current_quest = "battle_with_friend"
            for j in range(i+1, min(i+5, len(lines))):
                if "/" in lines[j] and any(c.isdigit() for c in lines[j]):
                    try:
                        parts = lines[j].split("/")
                        current = int(''.join(filter(str.isdigit, parts[0])))
                        total = int(''.join(filter(str.isdigit, parts[1])))
                        active_quests[current_quest] = {"current": current, "total": total}
                    except:
                        pass
                    break
        elif "action from a friend" in line_lower:
            current_quest = "action_from_friend"
            for j in range(i+1, min(i+5, len(lines))):
                if "/" in lines[j] and any(c.isdigit() for c in lines[j]):
                    try:
                        parts = lines[j].split("/")
                        current = int(''.join(filter(str.isdigit, parts[0])))
                        total = int(''.join(filter(str.isdigit, parts[1])))
                        active_quests[current_quest] = {"current": current, "total": total}
                    except:
                        pass
                    break
        elif "send an action to a friend" in line_lower or "use an action command" in line_lower:
            current_quest = "send_action"
            for j in range(i+1, min(i+5, len(lines))):
                if "/" in lines[j] and any(c.isdigit() for c in lines[j]):
                    try:
                        parts = lines[j].split("/")
                        current = int(''.join(filter(str.isdigit, parts[0])))
                        total = int(''.join(filter(str.isdigit, parts[1])))
                        active_quests[current_quest] = {"current": current, "total": total}
                    except:
                        pass
                    break
        elif "receive cookies" in line_lower or "receive a cookie" in line_lower:
            current_quest = "receive_cookie"
            for j in range(i+1, min(i+5, len(lines))):
                if "/" in lines[j] and any(c.isdigit() for c in lines[j]):
                    try:
                        parts = lines[j].split("/")
                        current = int(''.join(filter(str.isdigit, parts[0])))
                        total = int(''.join(filter(str.isdigit, parts[1])))
                        active_quests[current_quest] = {"current": current, "total": total}
                    except:
                        pass
                    break
        elif "receive curses" in line_lower or "curse you" in line_lower:
            current_quest = "receive_curses"
            for j in range(i+1, min(i+5, len(lines))):
                if "/" in lines[j] and any(c.isdigit() for c in lines[j]):
                    try:
                        parts = lines[j].split("/")
                        current = int(''.join(filter(str.isdigit, parts[0])))
                        total = int(''.join(filter(str.isdigit, parts[1])))
                        active_quests[current_quest] = {"current": current, "total": total}
                    except:
                        pass
                    break
        elif "receive prayers" in line_lower or "pray to you" in line_lower:
            current_quest = "receive_prayers"
            for j in range(i+1, min(i+5, len(lines))):
                if "/" in lines[j] and any(c.isdigit() for c in lines[j]):
                    try:
                        parts = lines[j].split("/")
                        current = int(''.join(filter(str.isdigit, parts[0])))
                        total = int(''.join(filter(str.isdigit, parts[1])))
                        active_quests[current_quest] = {"current": current, "total": total}
                    except:
                        pass
                    break
        elif "say 'owo'" in line_lower or "say owo" in line_lower:
            current_quest = "say_owo"
            for j in range(i+1, min(i+5, len(lines))):
                if "/" in lines[j] and any(c.isdigit() for c in lines[j]):
                    try:
                        parts = lines[j].split("/")
                        current = int(''.join(filter(str.isdigit, parts[0])))
                        total = int(''.join(filter(str.isdigit, parts[1])))
                        active_quests[current_quest] = {"current": current, "total": total}
                    except:
                        pass
                    break
        elif "gamble your cowoncy" in line_lower or "gamble" in line_lower:
            current_quest = "gamble_cowoncy"
            for j in range(i+1, min(i+5, len(lines))):
                if "/" in lines[j] and any(c.isdigit() for c in lines[j]):
                    try:
                        parts = lines[j].split("/")
                        current = int(''.join(filter(str.isdigit, parts[0])))
                        total = int(''.join(filter(str.isdigit, parts[1])))
                        active_quests[current_quest] = {"current": current, "total": total}
                    except:
                        pass
                    break

    has_completed = "CLAIMED" in full_text
    for quest, data in active_quests.items():
        if data["current"] >= data["total"]:
            has_completed = True
            
    claim_targets = []
    find_button_by_label(raw_data.get('components', []), "Claim", claim_targets)
    
    if claim_targets:
        claim_btn = claim_targets[0]
        if not claim_btn.get("disabled", False):
            log_worker_event(ws.worker_number, "Clicking Claim Quests button!", "SUCCESS")
            try:
                ws.error_claiming = False
                await _wrapped_interaction(
                    bs_msg._state,
                    _generate_nonce(),
                    InteractionType.component,
                    None,
                    bs_msg.channel,
                    claim_btn,
                    message=bs_msg
                )
                await asyncio.sleep(2)
                return await fetch_and_parse_quests(ctx, ws, bot)
            except Exception as e:
                log_worker_event(ws.worker_number, f"Error clicking Claim: {e}", "WARNING")
                ws.error_claiming = True

    SaveQuestsDataGhoStys(ws, active_quests)
    log_worker_event(ws.worker_number, f"Fetched quests: {active_quests}", "DEBUG")
    return active_quests

async def check_and_handle_quests(ctx, ws, bot):
    if manager.total_workers <= 1:
        return

    if not hasattr(ws, 'quests_enabled'):
        ws.quests_enabled = True
        ws.next_quest_check_time = datetime.now()
        ws.next_friend_battle_time = datetime.now()
        ws.friend_battle_helper_id = None
        
    if not ws.quests_enabled:
        return

    if datetime.now() >= getattr(ws, 'next_quest_check_time', datetime.min):
        active_quests = await fetch_and_parse_quests(ctx, ws, bot)
        if getattr(ws, 'error_claiming', False):
            ws.next_quest_check_time = datetime.now() + timedelta(minutes=2)
            ws.error_claiming = False
            log_worker_event(ws.worker_number, "Claiming failed, scheduled retry in 2 minutes.", "DEBUG")
        elif not getattr(ws, 'all_quests_finished', False):
            ws.next_quest_check_time = datetime.now() + timedelta(minutes=20)
    else:
        active_quests = LoadGhoStysQuestsData(ws)

    if not active_quests:
        return

    if "battle_with_friend" in active_quests:
        qdata = active_quests["battle_with_friend"]
        if qdata["current"] < qdata["total"]:
            if datetime.now() >= ws.next_friend_battle_time:
                if getattr(ws, 'busy_with_quest', False):
               
                    return
                    
                helper = manager.try_claim_friend_battle_helper(ws.worker_number)
                        
                if helper and helper.bot and helper.bot.user:
                    log_worker_event(ws.worker_number, f"Executing friend battle with {helper.username} ({helper.bot.user.id})", "INFO")
                    
                    ws.friend_battle_helper_id = helper.worker_number
                  
                    
                    helper.paused = True
                    helper.pause_end_time = datetime.now() + timedelta(minutes=2)
                    ws.paused = True
                    ws.pause_end_time = datetime.now() + timedelta(minutes=2)
                    
                    await asyncio.sleep(2)
                    await ctx.send(f"owo b <@{helper.bot.user.id}>")
                    
                    await asyncio.sleep(2.5)
                    
                    helper_channel = helper.bot.get_channel(ctx.channel.id)
                    if helper_channel:
                        asyncio.run_coroutine_threadsafe(helper_channel.send("owo ab"), helper.bot.loop)
                        log_worker_event(ws.worker_number, f"Commanded helper to send 'owo ab'", "DEBUG")
                    else:
                        log_worker_event(ws.worker_number, "Helper cannot see this channel to accept the battle!", "WARNING")
                    
                    await asyncio.sleep(15)
                    
                    helper.paused = False
                    helper.pause_end_time = None
                    helper.busy_with_quest = False
                    
                    ws.paused = False
                    ws.pause_end_time = None
                    ws.busy_with_quest = False
                    ws.friend_battle_helper_id = None
                    
                    qdata["current"] += 1
                    SaveQuestsDataGhoStys(ws, active_quests)
                    
                    log_worker_event(ws.worker_number, f"Friend battle done! Progress: {qdata['current']}/{qdata['total']}", "SUCCESS")
                    
                    if qdata["current"] >= qdata["total"]:
                        await fetch_and_parse_quests(ctx, ws, bot)
                    else:
                        delay_mins = random.randint(5, 15)
                        ws.next_friend_battle_time = datetime.now() + timedelta(minutes=delay_mins)
                        log_worker_event(ws.worker_number, f"Next friend battle scheduled in {delay_mins} minutes.", "DEBUG")
                else:
                    log_worker_event(ws.worker_number, "No idle helper worker available for battle quest right now. Will retry later.", "DEBUG")
                    ws.next_friend_battle_time = datetime.now() + timedelta(minutes=2)

    if "action_from_friend" in active_quests:
        qdata = active_quests["action_from_friend"]
        if qdata["current"] < qdata["total"]:
            if not hasattr(ws, 'next_action_quest_time'):
                ws.next_action_quest_time = datetime.now()
                
            if datetime.now() >= ws.next_action_quest_time:
                needed = qdata["total"] - qdata["current"]
                helpers = manager.get_action_helpers(ws.worker_number, needed)
                
                if helpers:
                    log_worker_event(ws.worker_number, f"Found {len(helpers)} helpers for action quest.", "INFO")
                    actions = ["punch", "slap", "pat", "hug", "kiss", "cuddle"]
                    
                    for helper in helpers:
                        action = random.choice(actions)
                        helper_channel = getattr(helper, 'zoo_channel', None)
                        if not helper_channel:
                            helper_channel = helper.bot.get_channel(getattr(helper, 'active_channel_id', None))
                            
                        if helper_channel:
                            asyncio.run_coroutine_threadsafe(
                                helper_channel.send(f"owo {action} <@{ws.bot.user.id}>"),
                                helper.bot.loop
                            )
                            qdata["current"] += 1
                        else:
                            log_worker_event(ws.worker_number, "Helper has no active channel to send action.", "DEBUG")
                            
                    SaveQuestsDataGhoStys(ws, active_quests)
                    log_worker_event(ws.worker_number, f"Action quest progress: {qdata['current']}/{qdata['total']}", "SUCCESS")
                    
                    if qdata["current"] >= qdata["total"]:
                        asyncio.create_task(fetch_and_parse_quests(ctx, ws, bot))
                    else:
                        delay_mins = random.randint(3, 8)
                        ws.next_action_quest_time = datetime.now() + timedelta(minutes=delay_mins)
                        log_worker_event(ws.worker_number, f"Next action quest retry in {delay_mins} mins.", "DEBUG")
                else:
                    log_worker_event(ws.worker_number, "No helpers available for action quest right now. Will retry later.", "DEBUG")
                    ws.next_action_quest_time = datetime.now() + timedelta(minutes=2)

    if "receive_cookie" in active_quests:
        qdata = active_quests["receive_cookie"]
        if qdata["current"] < qdata["total"]:
            if not hasattr(ws, 'next_cookie_quest_time'):
                ws.next_cookie_quest_time = datetime.now()
                
            if datetime.now() >= ws.next_cookie_quest_time:
                needed = qdata["total"] - qdata["current"]
                helpers = manager.get_cookie_helpers(ws.worker_number, needed)
                
                if helpers:
                    log_worker_event(ws.worker_number, f"Found {len(helpers)} helpers for cookie quest.", "INFO")
                    
                    for helper in helpers:
                        helper_channel = getattr(helper, 'zoo_channel', None)
                        if not helper_channel:
                            helper_channel = helper.bot.get_channel(getattr(helper, 'active_channel_id', None))
                            
                        if helper_channel:
                            asyncio.run_coroutine_threadsafe(
                                helper_channel.send(f"owo rep <@{ws.bot.user.id}>"),
                                helper.bot.loop
                            )
                            qdata["current"] += 1
                        else:
                            log_worker_event(ws.worker_number, "Helper has no active channel to send cookie.", "DEBUG")
                            
                    SaveQuestsDataGhoStys(ws, active_quests)
                    log_worker_event(ws.worker_number, f"Cookie quest progress (optimistic): {qdata['current']}/{qdata['total']}", "SUCCESS")
                    
                    if qdata["current"] >= qdata["total"]:
                        asyncio.get_event_loop().call_later(5.0, lambda: asyncio.create_task(fetch_and_parse_quests(ctx, ws, bot)))
                    else:
                        delay_mins = random.randint(3, 8)
                        ws.next_cookie_quest_time = datetime.now() + timedelta(minutes=delay_mins)
                        log_worker_event(ws.worker_number, f"Next cookie quest retry in {delay_mins} mins.", "DEBUG")
                else:
                    log_worker_event(ws.worker_number, "No helpers available for cookie quest right now. Will retry later.", "DEBUG")
                    ws.next_cookie_quest_time = datetime.now() + timedelta(minutes=5)

    if "receive_curses" in active_quests:
        qdata = active_quests["receive_curses"]
        if qdata["current"] < qdata["total"]:
            if not hasattr(ws, 'next_curse_quest_time'):
                ws.next_curse_quest_time = datetime.now()
                
            if datetime.now() >= ws.next_curse_quest_time:
                needed = qdata["total"] - qdata["current"]
                helpers = manager.get_pray_curse_helpers(ws.worker_number, needed)
                
                if helpers:
                    log_worker_event(ws.worker_number, f"Found {len(helpers)} helpers for curse quest.", "INFO")
                    
                    for helper in helpers:
                        helper_channel = getattr(helper, 'zoo_channel', None)
                        if not helper_channel:
                            helper_channel = helper.bot.get_channel(getattr(helper, 'active_channel_id', None))
                            
                        if helper_channel:
                            asyncio.run_coroutine_threadsafe(
                                helper_channel.send(f"owo curse <@{ws.bot.user.id}>"),
                                helper.bot.loop
                            )
                            qdata["current"] += 1
                        else:
                            log_worker_event(ws.worker_number, "Helper has no active channel to send curse.", "DEBUG")
                            
                    SaveQuestsDataGhoStys(ws, active_quests)
                    log_worker_event(ws.worker_number, f"Curse quest progress: {qdata['current']}/{qdata['total']}", "SUCCESS")
                    
                    if qdata["current"] >= qdata["total"]:
                        asyncio.get_event_loop().call_later(5.0, lambda: asyncio.create_task(fetch_and_parse_quests(ctx, ws, bot)))
                    else:
                        delay_mins = 5
                        ws.next_curse_quest_time = datetime.now() + timedelta(minutes=delay_mins, seconds=15)
                        log_worker_event(ws.worker_number, f"Next curse quest retry in {delay_mins} mins.", "DEBUG")
                else:
                    log_worker_event(ws.worker_number, "No helpers available for curse quest right now. Will retry later.", "DEBUG")
                    ws.next_curse_quest_time = datetime.now() + timedelta(minutes=2)

    if "receive_prayers" in active_quests:
        qdata = active_quests["receive_prayers"]
        if qdata["current"] < qdata["total"]:
            if not hasattr(ws, 'next_pray_quest_time'):
                ws.next_pray_quest_time = datetime.now()
                
            if datetime.now() >= ws.next_pray_quest_time:
                needed = qdata["total"] - qdata["current"]
                helpers = manager.get_pray_curse_helpers(ws.worker_number, needed)
                
                if helpers:
                    log_worker_event(ws.worker_number, f"Found {len(helpers)} helpers for pray quest.", "INFO")
                    
                    for helper in helpers:
                        helper_channel = getattr(helper, 'zoo_channel', None)
                        if not helper_channel:
                            helper_channel = helper.bot.get_channel(getattr(helper, 'active_channel_id', None))
                            
                        if helper_channel:
                            asyncio.run_coroutine_threadsafe(
                                helper_channel.send(f"owo pray <@{ws.bot.user.id}>"),
                                helper.bot.loop
                            )
                            qdata["current"] += 1
                        else:
                            log_worker_event(ws.worker_number, "Helper has no active channel to send pray.", "DEBUG")
                            
                    SaveQuestsDataGhoStys(ws, active_quests)
                    log_worker_event(ws.worker_number, f"Pray quest progress: {qdata['current']}/{qdata['total']}", "SUCCESS")
                    
                    if qdata["current"] >= qdata["total"]:
                        asyncio.get_event_loop().call_later(5.0, lambda: asyncio.create_task(fetch_and_parse_quests(ctx, ws, bot)))
                    else:
                        delay_mins = 5
                        ws.next_pray_quest_time = datetime.now() + timedelta(minutes=delay_mins, seconds=15)
                        log_worker_event(ws.worker_number, f"Next pray quest retry in {delay_mins} mins.", "DEBUG")
                else:
                    log_worker_event(ws.worker_number, "No helpers available for pray quest right now. Will retry later.", "DEBUG")
                    ws.next_pray_quest_time = datetime.now() + timedelta(minutes=2)

    if "say_owo" in active_quests:
        qdata = active_quests["say_owo"]
        if qdata["current"] < qdata["total"]:
            if not hasattr(ws, 'next_say_owo_time'):
                ws.next_say_owo_time = datetime.now()
                
            if datetime.now() >= ws.next_say_owo_time:
                await ctx.send("OwO")
                
                qdata["current"] += 1
                SaveQuestsDataGhoStys(ws, active_quests)
                
                log_worker_event(ws.worker_number, f"Say OwO quest progress: {qdata['current']}/{qdata['total']}", "SUCCESS")
                
                if qdata["current"] >= qdata["total"]:
                    asyncio.get_event_loop().call_later(5.0, lambda: asyncio.create_task(fetch_and_parse_quests(ctx, ws, bot)))
                else:
                    ws.next_say_owo_time = datetime.now() + timedelta(minutes=2)
                    log_worker_event(ws.worker_number, f"Next say OwO scheduled in 2 minutes.", "DEBUG")

    if "send_action" in active_quests:
        qdata = active_quests["send_action"]
        if qdata["current"] < qdata["total"]:
            if not hasattr(ws, 'next_send_action_time'):
                ws.next_send_action_time = datetime.now()
                
            if datetime.now() >= ws.next_send_action_time:
                target_id = None
                workers = manager.get_all_workers()
                if len(workers) > 1:
                    targets = [w.bot.user.id for w_num, w in workers.items() if w_num != ws.worker_number and w.bot and w.bot.user]
                    if targets:
                        target_id = random.choice(targets)
                        
                if target_id:
                    actions = ["punch", "slap", "pat", "hug", "kiss", "cuddle"]
                    action = random.choice(actions)
                    
                    await ctx.send(f"owo {action} <@{target_id}>")
                    
                    qdata["current"] += 1
                    SaveQuestsDataGhoStys(ws, active_quests)
                    
                    log_worker_event(ws.worker_number, f"Send action quest progress: {qdata['current']}/{qdata['total']}", "SUCCESS")
                    
                    if qdata["current"] >= qdata["total"]:
                        asyncio.get_event_loop().call_later(5.0, lambda: asyncio.create_task(fetch_and_parse_quests(ctx, ws, bot)))
                    else:
                        ws.next_send_action_time = datetime.now() + timedelta(minutes=1, seconds=36)
                        log_worker_event(ws.worker_number, f"Next send action scheduled in 1.6 minutes.", "DEBUG")
                else:
                    log_worker_event(ws.worker_number, "No target available for send action quest. Retrying in 2 mins.", "DEBUG")
                    ws.next_send_action_time = datetime.now() + timedelta(minutes=2)

    if "gamble_cowoncy" in active_quests:
        qdata = active_quests["gamble_cowoncy"]
        if qdata["current"] < qdata["total"]:
            if not hasattr(ws, 'next_gamble_quest_time'):
                ws.next_gamble_quest_time = datetime.now()
                
            if datetime.now() >= ws.next_gamble_quest_time:
                action = random.choice(["cf", "s"])
                await ctx.send(f"owo {action} 1")
                
                qdata["current"] += 1
                SaveQuestsDataGhoStys(ws, active_quests)
                
                log_worker_event(ws.worker_number, f"Gamble quest progress: {qdata['current']}/{qdata['total']}", "SUCCESS")
                
                if qdata["current"] >= qdata["total"]:
                    asyncio.get_event_loop().call_later(5.0, lambda: asyncio.create_task(fetch_and_parse_quests(ctx, ws, bot)))
                else:
                    ws.next_gamble_quest_time = datetime.now() + timedelta(minutes=2)
                    log_worker_event(ws.worker_number, f"Next gamble scheduled in 2 minutes.", "DEBUG")
''',
    'core/ui.py': r'''"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty OwO V4 Alpha Build
Stable Alpha Build Version: 280826.4.1.0

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

import sys
import os
import re
import shutil
import ctypes
from collections import deque
import time

GLOBAL_LOGS = deque(maxlen=2000)

def _push_log(worker_num, level, msg, full_str):
    GLOBAL_LOGS.append({
        "timestamp": time.time(),
        "worker": str(worker_num) if worker_num is not None else "SYSTEM",
        "level": level,
        "msg": msg,
        "formatted": strip_ansi(full_str)
    })

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

def _enable_windows_vt():
    if os.name == 'nt':
        try:
            kernel32 = ctypes.windll.kernel32
            handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                mode.value |= 0x0004 
                kernel32.SetConsoleMode(handle, mode)
        except Exception:
            pass

_enable_windows_vt()

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
ITALIC = "\033[3m"

CYAN_ELECTRIC = (0, 245, 255)
CYAN_MID      = (0, 195, 255)
BLUE_ELECTRIC = (30, 144, 255)
BLUE_NEON     = (59, 130, 246)
PURPLE_NEON   = (168, 85, 247)
PURPLE_LIGHT  = (192, 132, 252)
GREEN_NEON    = (52, 211, 153)
GREEN_EMERALD = (16, 185, 129)
YELLOW_GOLD   = (250, 204, 21)
RED_CRIMSON   = (248, 113, 113)
RED_BRIGHT    = (239, 68, 68)
GRAY_TEXT     = (148, 163, 184)
GRAY_MUTED    = (100, 116, 139)
GRAY_BORDER   = (51, 65, 85)
WHITE_BRIGHT  = (248, 250, 252)

def fg_rgb(r: int, g: int, b: int) -> str:
    return f"\033[38;2;{r};{g};{b}m"

def bg_rgb(r: int, g: int, b: int) -> str:
    return f"\033[48;2;{r};{g};{b}m"

def strip_ansi(text: str) -> str:
    return re.sub(r'\033\[[0-9;]*[a-zA-Z]', '', text)

def get_term_width(default: int = 86) -> int:
    try:
        w = shutil.get_terminal_size((default, 24)).columns
        return max(w, 60)
    except Exception:
        return default

def clear_screen():
    if os.name == "nt":
        os.system("cls")
    else:
        sys.stdout.write("\033[2J\033[H\033[3J")
        sys.stdout.flush()

def center(text: str, width: int = None) -> str:
    if width is None:
        width = get_term_width()
    plain_len = len(strip_ansi(text))
    if plain_len >= width:
        return text
    pad = (width - plain_len) // 2
    return " " * pad + text

def center_block(lines: list, width: int = None) -> list:
    if width is None:
        width = get_term_width()
    clean_lines = [strip_ansi(l) for l in lines]
    non_empty = [l for l in clean_lines if l.strip()]
    if not non_empty:
        return lines
    max_len = max(len(l) for l in non_empty)
    pad = max(0, (width - max_len) // 2)
    return [(" " * pad + line) if line.strip() else "" for line in lines]

def lerp_color(c1: tuple, c2: tuple, t: float) -> tuple:
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )

def multi_gradient_color(colors: list, t: float) -> tuple:
    if not colors:
        return (255, 255, 255)
    if len(colors) == 1 or t <= 0.0:
        return colors[0]
    if t >= 1.0:
        return colors[-1]
    
    seg_len = 1.0 / (len(colors) - 1)
    seg_idx = min(int(t / seg_len), len(colors) - 2)
    local_t = (t - (seg_idx * seg_len)) / seg_len
    return lerp_color(colors[seg_idx], colors[seg_idx + 1], local_t)

def colorize_gradient(text: str, colors: list = None) -> str:
    if colors is None:
        colors = [CYAN_ELECTRIC, CYAN_MID, BLUE_ELECTRIC, PURPLE_NEON]
    
    clean = strip_ansi(text)
    if not clean:
        return text
    
    n = len(clean)
    result = []
    clean_idx = 0
    
    in_ansi = False
    ansi_buf = []
    
    for ch in text:
        if ch == '\033':
            in_ansi = True
            ansi_buf.append(ch)
            continue
        if in_ansi:
            ansi_buf.append(ch)
            if ch.isalpha():
                in_ansi = False
                result.append("".join(ansi_buf))
                ansi_buf = []
            continue
        
        t = clean_idx / max(n - 1, 1)
        r, g, b = multi_gradient_color(colors, t)
        result.append(f"{fg_rgb(r, g, b)}{ch}")
        clean_idx += 1
        
    result.append(RESET)
    return "".join(result)


LOGO_GHOSTY_OWO = [
    '   ▄▄▄▄▄▄ ▄▄▄            ▄▄▄▄▄                 ▄▄▄▄▄▄                ▄▄▄▄▄▄',
    ' ██▀▀  ▀█  ██           ▄██ ▀█  ▄█            ██▀  ▀██              ██▀  ▀██',
    '███        ██▀██  ██▀█▄  ▀██▄▄ ▀██▀▀██▀▀█▀   ███    ███ ▀██▀██▀██▀ ███    ███',
    '▀██   ▀██▀ ██ ██ ███ ██ ▄  ▀▀██ ██  ▀███     ▀██    ██▀  ▀█▄▀███   ▀██    ██▀',
    ' ▀▀█▄▄▄█▀ ▄██▄██▄ ██▄█▀ █▀█▄▄█▀ ██▄  ▀█       ▀██▄▄██▀    ██ ▀█     ▀██▄▄██▀',
    '                                   ▄▄▄▀',
    '                                   ▀▀▀',
]

def render_header(worker_count: int, channel_count: int, has_main_ctrl: bool, width: int = None):
    if width is None:
        width = get_term_width()
    
    lines_out = []
    lines_out.append("")
    
    grad_colors = [CYAN_ELECTRIC, (45, 190, 255), BLUE_ELECTRIC, PURPLE_NEON]
    banner_grad = [colorize_gradient(l, grad_colors) for l in LOGO_GHOSTY_OWO]
    lines_out.extend(center_block(banner_grad, width))
    lines_out.append("")
    lines_out.append("")
    
    v_tag = (
        f"{fg_rgb(*CYAN_MID)}{BOLD}GhoSty OwO V4.1{RESET} "
        f"{fg_rgb(*GRAY_MUTED)}•{RESET} {fg_rgb(*PURPLE_LIGHT)}Alpha Build (280826.4.1.0){RESET} "
        f"{fg_rgb(*GRAY_MUTED)}•{RESET} {fg_rgb(*GREEN_NEON)}{BOLD}Free Forever{RESET}"
    )
    lines_out.append(center(v_tag, width))
    lines_out.append("")
    
    ctrl_status = f"{fg_rgb(*GREEN_NEON)}ACTIVE{RESET}" if has_main_ctrl else f"{fg_rgb(*GRAY_MUTED)}STANDALONE{RESET}"
    ch_status = f"{fg_rgb(*GREEN_NEON)}{channel_count} BOUND{RESET}" if channel_count > 0 else f"{fg_rgb(*YELLOW_GOLD)}MANUAL{RESET}"
    
    meta_line = (
        f"{fg_rgb(*GRAY_TEXT)}CONFIG: {RESET}{fg_rgb(*CYAN_ELECTRIC)}[config.json]{RESET}  "
        f"{fg_rgb(*GRAY_BORDER)}│{RESET}  {fg_rgb(*GRAY_TEXT)}WORKERS: {RESET}{fg_rgb(*CYAN_ELECTRIC)}<{worker_count}>{RESET}  "
        f"{fg_rgb(*GRAY_BORDER)}│{RESET}  {fg_rgb(*GRAY_TEXT)}CHANNELS: {RESET}{ch_status}  "
        f"{fg_rgb(*GRAY_BORDER)}│{RESET}  {fg_rgb(*GRAY_TEXT)}MAIN CTRL: {RESET}{ctrl_status}"
    )
    lines_out.append(center(meta_line, width))
    
    author_line = (
        f"{fg_rgb(*GRAY_MUTED)}< Made With {RESET}{fg_rgb(*RED_CRIMSON)}♥{RESET}{fg_rgb(*GRAY_MUTED)} in India By {RESET}"
        f"{fg_rgb(*CYAN_MID)}{BOLD}@jijaghosty{RESET}{fg_rgb(*GRAY_MUTED)} • {RESET}"
        f"{fg_rgb(*PURPLE_NEON)}🇮🇳 Async Development{RESET}{fg_rgb(*GRAY_MUTED)} >{RESET}"
    )
    lines_out.append(center(author_line, width))
    lines_out.append("")
    
    local_ip = "127.0.0.1"
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
        
    dashboard_line = f"{fg_rgb(*GRAY_MUTED)}Access Dashboard: {RESET}{fg_rgb(*CYAN_ELECTRIC)}http://{local_ip}:8765{RESET}"
    lines_out.append(center(dashboard_line, width))
    lines_out.append("")
    
    box_lines = render_command_matrix(width=width)
    lines_out.extend(box_lines)
    lines_out.append("")
    
    div_title = f" {BOLD}{fg_rgb(*CYAN_ELECTRIC)}[ LIVE SESSION LOGS ]{RESET} "
    div_plain_len = len(strip_ansi(div_title))
    box_w = min(width - 4, 82)
    left_line_len = 4
    right_line_len = max(0, box_w - left_line_len - div_plain_len)
    
    section_div = f"{fg_rgb(*GRAY_BORDER)}{'─' * left_line_len}{RESET}{div_title}{fg_rgb(*GRAY_BORDER)}{'─' * right_line_len}{RESET}"
    lines_out.append(center(section_div, width))
    lines_out.append("")
    
    return "\n".join(lines_out)


def render_command_matrix(width: int = None) -> list:
    if width is None:
        width = get_term_width()
    
    box_w = min(width - 4, 82)
    if box_w < 60:
        box_w = 60
    
    b_col = fg_rgb(*CYAN_MID)
    tag_col = fg_rgb(*CYAN_ELECTRIC)
    
    col1 = [
        ("<01>", ".start [all/N]", "Start farm"),
        ("<02>", ".stop [all/N]",  "Halt worker"),
        ("<03>", ".status [N]",    "Worker stats"),
        ("<04>", ".workers",       "List all"),
    ]
    col2 = [
        ("<05>", ".speed [mode]",  "Change speed"),
        ("<06>", ".huntbot [on/off]", "Auto HB"),
        ("<07>", ".pause <time>",  "Pause farm"),
        ("<08>", ".resume",        "Resume farm"),
    ]
    col3 = [
        ("<09>", ".profit [N]",    "Zoo profit"),
        ("<10>", ".say <text>",    "Echo message"),
        ("<11>", ".help",          "Show guide"),
        ("<12>", "???",       "Soon?"),
    ]
    
    col_w = (box_w - 4) // 3
    
    lines = []
    top_border = f"{b_col}╭{'─' * (box_w - 2)}╮{RESET}"
    lines.append(center(top_border, width))
    
    title_text = f"{BOLD}{fg_rgb(*WHITE_BRIGHT)}ALL COMMANDS{RESET}"
    inner_pad = (box_w - 2 - len(strip_ansi(title_text))) // 2
    right_pad = box_w - 2 - len(strip_ansi(title_text)) - inner_pad
    lines.append(center(f"{b_col}│{RESET}{' ' * inner_pad}{title_text}{' ' * right_pad}{b_col}│{RESET}", width))
    
    sep_border = f"{b_col}├{'─' * (box_w - 2)}┤{RESET}"
    lines.append(center(sep_border, width))
    
    for r in range(4):
        c1_num, c1_cmd, c1_desc = col1[r]
        c2_num, c2_cmd, c2_desc = col2[r]
        c3_num, c3_cmd, c3_desc = col3[r]
        
        c1_str = f"{tag_col}{c1_num}{RESET} {fg_rgb(*WHITE_BRIGHT)}{c1_cmd:<15}{RESET}"
        c2_str = f"{tag_col}{c2_num}{RESET} {fg_rgb(*WHITE_BRIGHT)}{c2_cmd:<15}{RESET}"
        c3_str = f"{tag_col}{c3_num}{RESET} {fg_rgb(*WHITE_BRIGHT)}{c3_cmd:<14}{RESET}"
        
        raw_c1_len = len(strip_ansi(c1_str))
        raw_c2_len = len(strip_ansi(c2_str))
        raw_c3_len = len(strip_ansi(c3_str))
        
        row_content = (
            f" {c1_str}{' ' * max(0, col_w - raw_c1_len)}"
            f"{b_col}│{RESET} {c2_str}{' ' * max(0, col_w - raw_c2_len)}"
            f"{b_col}│{RESET} {c3_str}"
        )
        
        row_plain_len = len(strip_ansi(row_content))
        r_pad = max(0, box_w - 2 - row_plain_len)
        lines.append(center(f"{b_col}│{RESET}{row_content}{' ' * r_pad}{b_col}│{RESET}", width))
    
    bottom_border = f"{b_col}╰{'─' * (box_w - 2)}╯{RESET}"
    lines.append(center(bottom_border, width))
    return lines

def make_badge(text: str, bg_tuple: tuple, fg_tuple: tuple = (0, 0, 0), width: int = 10) -> str:
    padded = f" {text} ".center(width)
    return f"{bg_rgb(*bg_tuple)}{fg_rgb(*fg_tuple)}{BOLD}{padded}{RESET}"

def log_support_prompt(width: int = None):
    if width is None:
        width = get_term_width()
    b_col = fg_rgb(*CYAN_ELECTRIC)
    t_col = fg_rgb(*WHITE_BRIGHT)
    l_col = fg_rgb(*PURPLE_NEON)
    
    print("")
    print(center(f"{b_col}╭────────────── [ ASYNC DEVELOPMENT COMMUNITY SUPPORT ] ──────────────╮{RESET}", width))
    print(center(f"{b_col}│{RESET} {fg_rgb(239, 68, 68)}{BOLD}[!] An unexpected error occurred in your session.{RESET}                      {b_col}│{RESET}", width))
    print(center(f"{b_col}│{RESET} {t_col}Join our official Discord server for instant help & updates:{RESET}           {b_col}│{RESET}", width))
    print(center(f"{b_col}│{RESET} {l_col}{BOLD}https://discord.gg/asMJGgDA7u{RESET}                                         {b_col}│{RESET}", width))
    print(center(f"{b_col}│{RESET} {fg_rgb(*GRAY_MUTED)}Made With ♥ By @jijaghosty • Async Development Support{RESET}                {b_col}│{RESET}", width))
    print(center(f"{b_col}╰──────────────────────────────────────────────────────────────────────╯{RESET}", width))
    print("")

def log_worker_event(worker_num, msg: str, level: str = "INFO"):
    if isinstance(worker_num, int):
        tag = f"{fg_rgb(*CYAN_ELECTRIC)}[ W#{worker_num:02d} ]{RESET}"
    elif str(worker_num).upper() in ["CTRL", "MAIN-CTRL", "MAIN"]:
        tag = f"{fg_rgb(*PURPLE_NEON)}[ MAIN-CTRL ]{RESET}"
    else:
        tag = f"{fg_rgb(*CYAN_ELECTRIC)}[{worker_num}]{RESET}"
    
    lvl = level.upper()
    if lvl == "INFO":
        badge = make_badge("INFO", (14, 165, 233), (0, 0, 0), width=10)
        arrow = f"{fg_rgb(*CYAN_MID)}──>{RESET}"
        msg_colored = f"{fg_rgb(*WHITE_BRIGHT)}{msg}{RESET}"
    elif lvl == "DEBUG":
        badge = make_badge("DEBUG", (99, 102, 241), (255, 255, 255), width=10)
        arrow = f"{fg_rgb(*BLUE_NEON)}──>{RESET}"
        msg_colored = f"{fg_rgb(*GRAY_TEXT)}{msg}{RESET}"
    elif lvl in ["SUCCESS", "HUNT", "SOLVED"]:
        badge = make_badge("SUCCESS", (16, 185, 129), (0, 0, 0), width=10)
        arrow = f"{fg_rgb(*GREEN_NEON)}──>{RESET}"
        msg_colored = f"{fg_rgb(*GREEN_NEON)}{msg}{RESET}"
    elif lvl in ["WARNING", "WARN"]:
        badge = make_badge("WARNING", (217, 119, 6), (0, 0, 0), width=10)
        arrow = f"{fg_rgb(*YELLOW_GOLD)}──>{RESET}"
        msg_colored = f"{fg_rgb(*YELLOW_GOLD)}{msg}{RESET}"
    elif lvl == "CRITICAL":
        badge = make_badge("CRITICAL", (153, 27, 27), (255, 255, 255), width=10)
        arrow = f"{fg_rgb(239, 68, 68)}──>{RESET}"
        msg_colored = f"{fg_rgb(248, 113, 113)}{BOLD}{msg}{RESET}"
    elif lvl in ["FATAL", "FATAL ERROR"]:
        badge = make_badge("FATAL", (185, 28, 28), (255, 255, 255), width=10)
        arrow = f"{fg_rgb(*RED_BRIGHT)}──>{RESET}"
        msg_colored = f"{fg_rgb(*RED_BRIGHT)}{BOLD}{msg}{RESET}"
    else:
        badge = make_badge(lvl[:8], (14, 165, 233), (0, 0, 0), width=10)
        arrow = f"{fg_rgb(*CYAN_MID)}──>{RESET}"
        msg_colored = f"{fg_rgb(*WHITE_BRIGHT)}{msg}{RESET}"
        
    full_str = f"   {badge} {tag} {arrow} {msg_colored}"
    print(full_str)
    _push_log(worker_num, lvl, msg, full_str)
    if lvl in ["CRITICAL", "FATAL", "FATAL ERROR"]:
        log_support_prompt()

def log_info(msg: str):
    badge = make_badge("INFO", (14, 165, 233), (0, 0, 0), width=10)
    arrow = f"{fg_rgb(*CYAN_MID)}──>{RESET}"
    full_str = f"   {badge} {arrow} {fg_rgb(*WHITE_BRIGHT)}{msg}{RESET}"
    print(full_str)
    _push_log("SYS", "INFO", msg, full_str)

def log_success(msg: str):
    badge = make_badge("READY", (16, 185, 129), (0, 0, 0), width=10)
    arrow = f"{fg_rgb(*GREEN_NEON)}──>{RESET}"
    full_str = f"   {badge} {arrow} {fg_rgb(*GREEN_NEON)}{msg}{RESET}"
    print(full_str)
    _push_log("SYS", "SUCCESS", msg, full_str)

def log_warn(msg: str):
    badge = make_badge("WARNING", (217, 119, 6), (0, 0, 0), width=10)
    arrow = f"{fg_rgb(*YELLOW_GOLD)}──>{RESET}"
    full_str = f"   {badge} {arrow} {fg_rgb(*YELLOW_GOLD)}{msg}{RESET}"
    print(full_str)
    _push_log("SYS", "WARN", msg, full_str)

def log_error(msg: str):
    badge = make_badge("ERROR", (220, 38, 38), (255, 255, 255), width=10)
    arrow = f"{fg_rgb(*RED_BRIGHT)}──>{RESET}"
    full_str = f"   {badge} {arrow} {fg_rgb(248, 113, 113)}{msg}{RESET}"
    print(full_str)
    _push_log("SYS", "ERROR", msg, full_str)

def log_critical(worker_label: str, error: Exception | str):
    badge = make_badge("CRITICAL", (153, 27, 27), (255, 255, 255), width=10)
    tag = f"{fg_rgb(*RED_CRIMSON)}{worker_label}{RESET}"
    arrow = f"{fg_rgb(*RED_CRIMSON)}──>{RESET}"
    msg = f"{fg_rgb(*RED_CRIMSON)}{error}{RESET}"
    print(f"   {badge} {tag} {arrow} {msg}")
    log_support_prompt()

def log_worker_start(worker_num: int):
    badge = make_badge("INIT", (6, 182, 212), (0, 0, 0), width=10)
    tag = f"{fg_rgb(*CYAN_ELECTRIC)}[ W#{worker_num:02d} ]{RESET}"
    arrow = f"{fg_rgb(*GRAY_MUTED)}──>{RESET}"
    msg = f"{fg_rgb(*CYAN_MID)}Initializing worker thread...{RESET}"
    print(f"   {badge} {tag} {arrow} {msg}")

def log_worker_ready(worker_num: int, username: str, channel_id: int = None):
    badge = make_badge("ONLINE", (16, 185, 129), (0, 0, 0), width=10)
    tag = f"{fg_rgb(*GREEN_NEON)}[ W#{worker_num:02d} ]{RESET}"
    arrow = f"{fg_rgb(*GREEN_NEON)}──>{RESET}"
    user_str = f"{fg_rgb(*WHITE_BRIGHT)}{BOLD}@{username}{RESET}"
    
    if channel_id:
        ch_str = f"{fg_rgb(*GRAY_MUTED)}(Channel: {fg_rgb(*CYAN_ELECTRIC)}{channel_id}{fg_rgb(*GRAY_MUTED)}){RESET}"
        print(f"   {badge} {tag} {arrow} Connected as {user_str} {ch_str}")
    else:
        no_ch = f"{fg_rgb(*YELLOW_GOLD)}(No channel assigned — use .start from account or main){RESET}"
        print(f"   {badge} {tag} {arrow} Connected as {user_str} {no_ch}")

def log_controller_ready(username: str):
    badge = make_badge("CTRL", (147, 51, 234), (255, 255, 255), width=10)
    tag = f"{fg_rgb(*PURPLE_NEON)}[ MAIN-CTRL ]{RESET}"
    arrow = f"{fg_rgb(*PURPLE_NEON)}──>{RESET}"
    user_str = f"{fg_rgb(*WHITE_BRIGHT)}{BOLD}@{username}{RESET}"
    print(f"   {badge} {tag} {arrow} Main Controller online as {user_str}")

def log_disconnect(worker_label: str):
    badge = make_badge("OFFLINE", (234, 88, 12), (0, 0, 0), width=10)
    tag = f"{fg_rgb(*YELLOW_GOLD)}{worker_label}{RESET}"
    arrow = f"{fg_rgb(*YELLOW_GOLD)}──>{RESET}"
    msg = f"{fg_rgb(*GRAY_TEXT)}Disconnected from Discord — auto-reconnecting...{RESET}"
    print(f"   {badge} {tag} {arrow} {msg}")

def log_resumed(worker_label: str):
    badge = make_badge("RESUMED", (16, 185, 129), (0, 0, 0), width=10)
    tag = f"{fg_rgb(*GREEN_NEON)}{worker_label}{RESET}"
    arrow = f"{fg_rgb(*GREEN_NEON)}──>{RESET}"
    msg = f"{fg_rgb(*GREEN_NEON)}Gateway connection resumed.{RESET}"
    print(f"   {badge} {tag} {arrow} {msg}")

def log_retry(worker_label: str, delay: int, attempt: int):
    badge = make_badge("RETRY", (202, 138, 4), (0, 0, 0), width=10)
    tag = f"{fg_rgb(*YELLOW_GOLD)}{worker_label}{RESET}"
    arrow = f"{fg_rgb(*YELLOW_GOLD)}──>{RESET}"
    msg = f"{fg_rgb(*GRAY_TEXT)}Reconnecting in {fg_rgb(*YELLOW_GOLD)}{delay}s{fg_rgb(*GRAY_TEXT)} (attempt #{attempt})...{RESET}"
    print(f"   {badge} {tag} {arrow} {msg}")

def log_fatal_error(worker_label: str, error: Exception):
    badge = make_badge("FATAL", (185, 28, 28), (255, 255, 255), width=10)
    tag = f"{fg_rgb(*RED_BRIGHT)}{worker_label}{RESET}"
    arrow = f"{fg_rgb(*RED_BRIGHT)}──>{RESET}"
    msg = f"{fg_rgb(*RED_BRIGHT)}Auth error (token invalid/banned) — worker stopped: {error}{RESET}"
    print(f"   {badge} {tag} {arrow} {msg}")
    log_support_prompt()

def log_net_error(worker_label: str, error: Exception):
    badge = make_badge("NET_ERR", (202, 138, 4), (0, 0, 0), width=10)
    tag = f"{fg_rgb(*YELLOW_GOLD)}{worker_label}{RESET}"
    arrow = f"{fg_rgb(*YELLOW_GOLD)}──>{RESET}"
    msg = f"{fg_rgb(*GRAY_TEXT)}Network error ({type(error).__name__}): {error} — will retry{RESET}"
    print(f"   {badge} {tag} {arrow} {msg}")

def log_event_error(worker_label: str, event: str):
    badge = make_badge("ERROR", (220, 38, 38), (255, 255, 255), width=10)
    tag = f"{fg_rgb(*RED_BRIGHT)}{worker_label}{RESET}"
    arrow = f"{fg_rgb(*RED_BRIGHT)}──>{RESET}"
    print(f"   {badge} {tag} {arrow} Error in '{event}'")

def log_shutdown():
    badge = make_badge("SHUTDOWN", (220, 38, 38), (255, 255, 255), width=10)
    print(f"\n   {badge} {fg_rgb(*RED_BRIGHT)}Shutting down all active workers and threads...{RESET}")

''',
    'core/utils.py': r'''"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty OwO V4 Alpha Build
Stable Alpha Build Version: 280826.4.1.0

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

import asyncio
import discord
from discord.ext import commands
from colorama import Fore, Style

GhoStyyy = "."

def create_bot(worker_number):
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    bot = commands.Bot(
        command_prefix=GhoStyyy, case_insensitive=True, self_bot=True
    )
    bot.remove_command("help")
    bot.worker_number = worker_number
    return bot''',
    'dashboard/app.py': r'''
"""
This code is only made for educational and practice purposes. 
Author and Async Development are not responsible for misuse.

GhoSty OwO V4 Alpha Build
Stable Alpha Build Version: 280826.4.1.0

GitHub: https://github.com/WannaBeGhoSt
Discord: https://discord.gg/asMJGgDA7u
"""

import os
import sys
import json
import traceback
import subprocess
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from core.heart import manager
from core.ui import GLOBAL_LOGS

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "dashboard", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "dashboard", "static")

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app)

from flask import Flask, jsonify, request, render_template, send_from_directory

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/assets/<path:filename>")
def serve_assets(filename):
    return send_from_directory(os.path.join(BASE_DIR, "assets"), filename)

@app.route("/api/status", methods=["GET"])
def get_status():
    workers = manager.get_all_workers()
    data = {}
    total_cash = 0
    total_essence = 0
    active_workers = 0

    quests_data = {}
    quests_path = os.path.join(BASE_DIR, "ghostyworkerquests.json")
    if os.path.exists(quests_path):
        try:
            with open(quests_path, "r", encoding="utf-8") as f:
                quests_data = json.load(f)
        except:
            pass

    for w_num, w in workers.items():
        w_dict = w.to_dict()
        w_dict["quests"] = quests_data.get(str(w_num), {})
        
        total_cash += w.initial_cash or 0
        total_essence += w.initial_essence or 0
        
        if w.running and not w.paused and not w.sleep_mode:
            active_workers += 1
            
        data[w_num] = w_dict

    return jsonify({
        "workers": data,
        "summary": {
            "total_workers": len(workers),
            "active_workers": active_workers,
            "total_cash": total_cash,
            "total_essence": total_essence
        }
    })

@app.route("/api/logs", methods=["GET"])
def get_logs():
    worker_id = request.args.get("worker")
    logs = list(GLOBAL_LOGS)
    
    if worker_id and worker_id != "all":
        logs = [log for log in logs if log["worker"] == worker_id or log["worker"] == "SYS"]
        
    return jsonify(logs[-500:])

@app.route("/api/control/<worker_num>", methods=["POST"])
def control_worker(worker_num):
    action = request.json.get("action")
    if worker_num == "all":
        workers = manager.get_all_workers().values()
    else:
        try:
            w_num = int(worker_num)
            w = manager.get_worker(w_num)
            if w:
                workers = [w]
            else:
                return jsonify({"error": "Worker not found"}), 404
        except ValueError:
            return jsonify({"error": "Invalid worker ID"}), 400

    success_count = 0
    for w in workers:
        if action == "start":
            if not w.running:
                import asyncio
                from core.heart import _run_farming_loop, PseudoCtx
                chan_id = getattr(w, 'auto_start_channel_id', None)
                if not chan_id:
                    from main import channels_map
                    chan_id = channels_map.get(w.worker_number)
                
                if chan_id and w.bot:
                    channel = w.bot.get_channel(chan_id)
                    if channel:
                        ctx = PseudoCtx(channel, w.bot)
                        asyncio.run_coroutine_threadsafe(_run_farming_loop(ctx, w, w.bot), w.bot.loop)
                        success_count += 1

        elif action == "pause":
            if w.running and not w.paused:
                time_str = request.json.get("time")
                import datetime
                if time_str:
                    from core.heart import _parse_pause_time
                    secs = _parse_pause_time(time_str)
                    if secs is not None and secs >= 900:
                        w.paused = True
                        w.pause_end_time = datetime.datetime.now() + datetime.timedelta(seconds=secs)
                        success_count += 1
                else:
                    w.paused = True
                    w.pause_end_time = datetime.datetime.now() + datetime.timedelta(days=365)
                    success_count += 1
        elif action == "resume":
            if w.running and w.paused:
                w.paused = False
                w.pause_end_time = None
                success_count += 1
        elif action == "stop":
            if w.running:
                w.running = False
                success_count += 1
        elif action == "speed":
            mode = request.json.get("mode")
            if mode in ["efficient", "fast", "durable", "lifetime", "humanoid"]:
                w.current_speed_mode = mode
                import datetime
                w.last_mode_change_time = datetime.datetime.now()
                success_count += 1
        elif action == "huntbot":
            toggle = request.json.get("toggle")
            if toggle in ["on", "off"]:
                w.huntbot_enabled = (toggle == "on")
                success_count += 1
        elif action == "mail":
            import datetime
            if w.last_mail_claim:
                time_since = (datetime.datetime.now() - w.last_mail_claim).total_seconds()
                if time_since < 300:
                    continue
            if not getattr(w, "is_mail_claiming", False):
                w.last_mail_claim = datetime.datetime.now()
                w.is_mail_claiming = True
                
                chan_id = w.auto_start_channel_id
                if chan_id and w.bot and w.bot.loop and w.bot.loop.is_running():
                    channel = w.bot.get_channel(chan_id)
                    if channel:
                        from core.heart import PseudoCtx
                        from core.mailmodule import execute_mail_claim
                        import asyncio
                        ctx = PseudoCtx(channel, w.bot)
                        w.bot.loop.create_task(execute_mail_claim(ctx, w, w.bot))
                        success_count += 1
                
    return jsonify({"success": True, "affected": success_count, "action": action})

@app.route("/api/profit", methods=["GET"])
def fetch_profit():
    from core.heart import manager
    try:
        from core.heart import _fetch_zoo_for_main_status
    except ImportError:
        return jsonify({"success": False, "error": "Could not import zoo fetcher"})
    
    import asyncio
    
    all_ws = manager.get_all_workers()
    futures = []
    
    for wn, target_ws in sorted(all_ws.items()):
        if (
            target_ws.has_started
            and target_ws.zoo_channel
            and not target_ws.sleep_mode
            and not target_ws.paused
            and getattr(target_ws, 'bot', None)
            and getattr(target_ws.bot, 'loop', None)
            and target_ws.bot.loop.is_running()
        ):
            try:
                future = asyncio.run_coroutine_threadsafe(
                    _fetch_zoo_for_main_status(target_ws),
                    target_ws.bot.loop,
                )
                futures.append(future)
            except Exception:
                pass
                
    for future in futures:
        try:
            future.result(timeout=10)
        except Exception:
            pass

    def format_value(value):
        if value >= 1_000_000:
            return f"{value / 1_000_000:.2f}M"
        elif value >= 1_000:
            return f"{value / 1_000:.2f}K"
        else:
            return f"{int(value)}"

    total_profit = 0
    worker_data = []

    for wn, target_ws in sorted(all_ws.items()):
        if not target_ws.has_started:
            worker_data.append({
                "worker": wn,
                "username": target_ws.username,
                "status": "Not started",
                "profit": 0,
                "profit_str": "0",
                "start_cash": 0,
                "current_cash": 0
            })
            continue

        profit = getattr(target_ws, 'current_cash', 0) - (target_ws.initial_cash or 0)
        total_profit += profit

        if target_ws.sleep_mode:
            status = "Sleeping"
        elif target_ws.paused:
            status = "Paused"
        elif not target_ws.running:
            status = "Stopped"
        else:
            status = "Running"

        worker_data.append({
            "worker": wn,
            "username": target_ws.username,
            "status": status,
            "profit": profit,
            "profit_str": format_value(profit),
            "start_cash": format_value(target_ws.initial_cash or 0),
            "current_cash": format_value(getattr(target_ws, 'current_cash', 0))
        })

    return jsonify({
        "success": True, 
        "workers": worker_data,
        "total_profit": total_profit,
        "total_profit_str": format_value(total_profit)
    })

@app.route("/api/say", methods=["POST"])
def say_command():
    text = request.json.get("text", "").strip()
    if not text:
        return jsonify({"success": False, "error": "No text provided"})
        
    from core.heart import manager
    import asyncio
    all_ws = manager.get_all_workers()
    sent = 0
    for wn, target_ws in sorted(all_ws.items()):
        ch_id = getattr(target_ws, 'auto_start_channel_id', None)
        if ch_id and getattr(target_ws, 'bot', None) and getattr(target_ws.bot, 'loop', None) and target_ws.bot.loop.is_running():
            channel = target_ws.bot.get_channel(ch_id)
            if channel:
                asyncio.run_coroutine_threadsafe(channel.send(text), target_ws.bot.loop)
                sent += 1
                
    return jsonify({"success": True, "sent": sent})

@app.route("/api/config", methods=["GET", "POST"])
def manage_config():
    tokens_path = os.path.join(BASE_DIR, "tokens.txt")
    channels_path = os.path.join(BASE_DIR, "channels.txt")
    
    if request.method == "POST":
        data = request.json
        if "tokens" in data:
            with open(tokens_path, "w", encoding="utf-8") as f:
                f.write(data["tokens"])
        if "channels" in data:
            with open(channels_path, "w", encoding="utf-8") as f:
                f.write(data["channels"])
        return jsonify({"success": True})
    
    tokens_content = ""
    channels_content = ""
    if os.path.exists(tokens_path):
        with open(tokens_path, "r", encoding="utf-8") as f:
            tokens_content = f.read()
    if os.path.exists(channels_path):
        with open(channels_path, "r", encoding="utf-8") as f:
            channels_content = f.read()
            
    return jsonify({
        "tokens": tokens_content,
        "channels": channels_content
    })

@app.route("/api/restart", methods=["POST"])
def restart_script():
    import threading
    import time
    
    def _restart():
        time.sleep(1)
        os.execv(sys.executable, ['python'] + sys.argv)
        
    threading.Thread(target=_restart).start()
    return jsonify({"success": True, "message": "Restarting script in 1 second..."})

def start_server():
    import logging
    import socket
    log = logging.getLogger('werkzeug')
    log.setLevel(logging.ERROR)
    
    local_ip = "127.0.0.1"
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        pass
        
    try:
        from waitress import serve
        serve(app, host='0.0.0.0', port=int(os.environ.get('PORT', '8765')))
    except ImportError:
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "8765")), debug=False, use_reloader=False)

if __name__ == "__main__":
    start_server()
''',
    'dashboard/static/css/style.css': r''':root {
    --bg-main: #0B0E14;
    --bg-card: #151A23;
    --bg-card-hover: #1A202C;
    --text-primary: #F8FAFC;
    --text-secondary: #94A3B8;
    --border-color: #1E293B;

    --primary: #6366F1;
    --primary-hover: #4F46E5;

    --success: #10B981;
    --warning: #F59E0B;
    --danger: #EF4444;
    --info: #3B82F6;

    --sidebar-width: 260px;
    --header-height: 70px;

    --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    --shadow-glow: 0 0 15px rgba(99, 102, 241, 0.15);
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', sans-serif;
    background-color: var(--bg-main);
    color: var(--text-primary);
    overflow-x: hidden;
    line-height: 1.5;
}

/* Sidebar */
.sidebar {
    position: fixed;
    top: 0;
    left: 0;
    width: var(--sidebar-width);
    height: 100vh;
    background-color: var(--bg-card);
    border-right: 1px solid var(--border-color);
    z-index: 100;
    transition: transform 0.3s ease;
}

.sidebar-header {
    height: var(--header-height);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 24px;
    border-bottom: 1px solid var(--border-color);
}

.brand {
    display: flex;
    align-items: center;
    gap: 12px;
}

.brand-icon {
    font-size: 24px;
    color: var(--primary);
    filter: drop-shadow(0 0 8px rgba(99, 102, 241, 0.4));
}

.brand-text h2 {
    font-size: 16px;
    font-weight: 700;
    line-height: 1.2;
}

.brand-text span {
    font-size: 11px;
    color: var(--text-secondary);
}

.mobile-close {
    display: none;
    background: none;
    border: none;
    color: var(--text-secondary);
    font-size: 20px;
    cursor: pointer;
}

.nav-menu {
    padding: 24px 16px;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 16px;
    background: transparent;
    border: none;
    border-radius: 8px;
    color: var(--text-secondary);
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s ease;
    font-family: 'Inter', sans-serif;
}

.nav-item:hover {
    background-color: var(--bg-card-hover);
    color: var(--text-primary);
}

.nav-item.active {
    background-color: rgba(99, 102, 241, 0.1);
    color: var(--primary);
    position: relative;
}

.nav-item.active::before {
    content: '';
    position: absolute;
    left: 0;
    top: 50%;
    transform: translateY(-50%);
    width: 4px;
    height: 20px;
    background-color: var(--primary);
    border-radius: 0 4px 4px 0;
}

.nav-item i {
    font-size: 16px;
    width: 20px;
    text-align: center;
}

/* Main Content */
.main-content {
    margin-left: var(--sidebar-width);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

.top-header {
    height: var(--header-height);
    background-color: rgba(21, 26, 35, 0.8);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 0 32px;
    position: sticky;
    top: 0;
    z-index: 90;
}

.mobile-toggle {
    display: none;
    background: none;
    border: none;
    color: var(--text-primary);
    font-size: 20px;
    cursor: pointer;
}

.header-title {
    font-size: 18px;
    font-weight: 600;
}

.status-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13px;
    color: var(--success);
    background-color: rgba(16, 185, 129, 0.1);
    padding: 6px 12px;
    border-radius: 20px;
    font-weight: 500;
}

.dot {
    width: 8px;
    height: 8px;
    background-color: var(--success);
    border-radius: 50%;
}

.pulse {
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0% {
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.4);
    }

    70% {
        box-shadow: 0 0 0 6px rgba(16, 185, 129, 0);
    }

    100% {
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0);
    }
}

.content-wrapper {
    padding: 32px;
    flex-grow: 1;
}

/* Tabs */
.tab-pane {
    display: none;
    animation: fadeIn 0.3s ease;
}

.tab-pane.active {
    display: block;
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Cards */
.card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    box-shadow: var(--shadow-md);
    overflow: hidden;
}

.card-header {
    padding: 20px 24px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.card-header h3 {
    font-size: 16px;
    font-weight: 600;
}

.card-body {
    padding: 24px;
}

/* Stats Grid */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 24px;
}

.stat-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 24px;
    display: flex;
    align-items: center;
    gap: 20px;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-glow);
}

.stat-icon {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}

.stat-icon.purple {
    background-color: rgba(99, 102, 241, 0.1);
    color: var(--primary);
}

.stat-icon.green {
    background-color: rgba(16, 185, 129, 0.1);
    color: var(--success);
}

.stat-icon.yellow {
    background-color: rgba(245, 158, 11, 0.1);
    color: var(--warning);
}

.stat-icon.cyan {
    background-color: rgba(59, 130, 246, 0.1);
    color: var(--info);
}

.stat-details h3 {
    font-size: 13px;
    color: var(--text-secondary);
    font-weight: 500;
    margin-bottom: 4px;
}

.stat-details h2 {
    font-size: 24px;
    font-weight: 700;
}

/* Buttons */
.btn {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 10px 16px;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    border: none;
    transition: all 0.2s ease;
    font-family: inherit;
}

.btn-sm {
    padding: 6px 12px;
    font-size: 12px;
}

.btn-primary {
    background-color: var(--primary);
    color: white;
}

.btn-primary:hover {
    background-color: var(--primary-hover);
}

.btn-warning {
    background-color: var(--warning);
    color: white;
}

.btn-warning:hover {
    filter: brightness(0.9);
}

.btn-danger {
    background-color: var(--danger);
    color: white;
}

.btn-danger:hover {
    filter: brightness(0.9);
}

.btn-outline {
    background-color: transparent;
    border: 1px solid var(--border-color);
    color: var(--text-primary);
}

.btn-outline:hover {
    background-color: var(--bg-card-hover);
}

.action-buttons {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
}

/* Tables */
.table-responsive {
    overflow-x: auto;
}

.status-table {
    width: 100%;
    border-collapse: collapse;
}

.status-table th,
.status-table td {
    padding: 16px;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

.status-table th {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--text-secondary);
    font-weight: 600;
}

.status-table td {
    font-size: 14px;
}

.status-table tbody tr:last-child td {
    border-bottom: none;
}

/* Badges */
.badge {
    padding: 4px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    display: inline-block;
}

.badge-success {
    background-color: rgba(16, 185, 129, 0.1);
    color: var(--success);
}

.badge-warning {
    background-color: rgba(245, 158, 11, 0.1);
    color: var(--warning);
}

.badge-danger {
    background-color: rgba(239, 68, 68, 0.1);
    color: var(--danger);
}

.badge-info {
    background-color: rgba(59, 130, 246, 0.1);
    color: var(--info);
}

/* Control Grid */
.control-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
}

.worker-control-card {
    background-color: var(--bg-main);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 20px;
}

.wcc-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 16px;
}

.wcc-actions {
    display: flex;
    gap: 8px;
}

/* Console */
.console-card {
    height: 600px;
    display: flex;
    flex-direction: column;
}

.console-controls {
    display: flex;
    gap: 16px;
    align-items: center;
}

.form-select {
    background-color: var(--bg-main);
    color: var(--text-primary);
    border: 1px solid var(--border-color);
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
    outline: none;
}

.console-body {
    flex-grow: 1;
    overflow-y: auto;
    background-color: #050505;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    padding: 16px;
    white-space: pre-wrap;
    word-break: break-all;
}

.log-line {
    margin-bottom: 4px;
    line-height: 1.4;
}

.log-time {
    color: var(--text-secondary);
    margin-right: 12px;
}

.log-INFO {
    color: #38bdf8;
}

.log-SUCCESS {
    color: #34d399;
}

.log-WARN {
    color: #fbbf24;
}

.log-ERROR {
    color: #f87171;
}

.log-DEBUG {
    color: #818cf8;
}

/* Settings */
.grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 24px;
}

.form-textarea {
    width: 100%;
    background-color: var(--bg-main);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    color: var(--text-primary);
    padding: 16px;
    font-family: 'Consolas', 'Courier New', monospace;
    font-size: 13px;
    resize: vertical;
    outline: none;
}

.form-textarea:focus {
    border-color: var(--primary);
}

.danger-zone {
    border-color: rgba(239, 68, 68, 0.3);
}

/* Toggle Switch */
.toggle-switch {
    display: flex;
    align-items: center;
    cursor: pointer;
    gap: 8px;
    font-size: 13px;
}

.toggle-switch input {
    display: none;
}

.slider {
    width: 36px;
    height: 20px;
    background-color: var(--border-color);
    border-radius: 20px;
    position: relative;
    transition: 0.3s;
}

.slider::before {
    content: "";
    position: absolute;
    width: 14px;
    height: 14px;
    border-radius: 50%;
    background-color: white;
    top: 3px;
    left: 3px;
    transition: 0.3s;
}

.toggle-switch input:checked+.slider {
    background-color: var(--primary);
}

.toggle-switch input:checked+.slider::before {
    transform: translateX(16px);
}

/* Progress Bars */
.progress-bar-container {
    width: 100%;
    background-color: var(--border-color);
    border-radius: 10px;
    height: 8px;
    overflow: hidden;
    margin-top: 6px;
}

.progress-bar-fill {
    height: 100%;
    background-color: var(--primary);
    transition: width 0.3s ease;
}

.mt-2 {
    margin-top: 8px;
}

.mt-3 {
    margin-top: 16px;
}

.mt-4 {
    margin-top: 24px;
}

.mb-4 {
    margin-bottom: 24px;
}

.text-danger {
    color: var(--danger);
}

.text-muted {
    color: var(--text-secondary);
}

/* Responsive */
@media (max-width: 992px) {
    .grid-2 {
        grid-template-columns: 1fr;
    }
}

@media (max-width: 768px) {
    .sidebar {
        transform: translateX(-100%);
    }

    .sidebar.open {
        transform: translateX(0);
    }

    .main-content {
        margin-left: 0;
    }

    .mobile-toggle {
        display: block;
    }

    .mobile-close {
        display: block;
    }

    .top-header {
        padding: 0 16px;
    }

    .content-wrapper {
        padding: 16px;
    }

    .stats-grid {
        grid-template-columns: 1fr;
    }

    .console-controls {
        flex-wrap: wrap;
    }

    .hide-mobile,
    .hide-mobile-title {
        display: none !important;
    }

    .header-actions {
        gap: 6px !important;
    }

    .icon-only-mobile {
        padding: 6px 8px !important;
        gap: 0 !important;
    }
    
    .donate-btn-mobile {
        padding: 6px 10px !important;
        gap: 4px !important;
    }
}''',
    'dashboard/static/js/script.js': r'''const API_BASE = '/api';
let isAutoScroll = true;
let isStreamerMode = localStorage.getItem('ghostyStreamerMode') === 'true';

window.showToast = function (message, type = "success") {
    const container = document.getElementById('toast-container');
    if (!container) return;
    const toast = document.createElement('div');
    toast.style.padding = '12px 20px';
    toast.style.marginBottom = '10px';
    toast.style.borderRadius = '8px';
    toast.style.color = '#fff';
    toast.style.background = type === 'success' ? 'var(--success)' : 'var(--danger)';
    toast.style.boxShadow = '0 4px 6px -1px rgba(0, 0, 0, 0.1)';
    toast.style.transition = 'opacity 0.3s ease';
    toast.style.opacity = '0';
    toast.innerText = message;

    container.appendChild(toast);

    setTimeout(() => toast.style.opacity = '1', 10);

    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
};

window.controlAll = async function (action) {
    window.controlWorker('all', action);
};

window.controlWorker = async function (id, action) {
    try {
        await fetch(`${API_BASE}/control/${id}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ action })
        });
        window.fetchStatus();
        window.showToast(`Action '${action}' dispatched successfully!`, "success");
    } catch (e) {
        window.showToast("Action failed!", "error");
    }
};

window.applyControllerSettings = async function (settingType) {
    let workerId, payload = {};

    if (settingType === 'speed') {
        workerId = document.getElementById('ctrl-speed-worker').value;
        payload = { action: 'speed', mode: document.getElementById('ctrl-speed-mode').value };
    } else if (settingType === 'huntbot') {
        workerId = document.getElementById('ctrl-hb-worker').value;
        payload = { action: 'huntbot', toggle: document.getElementById('ctrl-hb-toggle').value };
    } else if (settingType === 'pause_time') {
        workerId = document.getElementById('ctrl-pause-worker').value;
        const timeVal = document.getElementById('ctrl-pause-time').value.trim();
        if (!timeVal) {
            window.showToast("Please enter a valid time (e.g., 30m, 1h)", "error");
            return;
        }
        payload = { action: 'pause', time: timeVal };
    } else if (settingType === 'mail') {
        workerId = document.getElementById('ctrl-mail-worker').value;
        payload = { action: 'mail' };
    }

    try {
        const res = await fetch(`${API_BASE}/control/${workerId}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        if (data.success) {
            window.showToast(`Settings applied to ${data.affected} worker(s)!`, "success");
            window.fetchStatus();
        } else {
            window.showToast("Failed to apply settings", "error");
        }
    } catch (e) {
        window.showToast("Error applying settings", "error");
    }
};

window.fetchStatus = async function () {
    try {
        const res = await fetch(`${API_BASE}/status`);
        const data = await res.json();
        document.getElementById('home-total-workers').innerText = data.summary.total_workers;
        document.getElementById('home-active-workers').innerText = data.summary.active_workers;
        document.getElementById('home-total-cowoncy').innerText = (data.summary.total_cash || 0).toLocaleString();
        document.getElementById('home-total-essence').innerText = (data.summary.total_essence || 0).toLocaleString();

        const statusGrid = document.getElementById('status-grid');
        const controlGrid = document.getElementById('control-grid');
        let statusHTML = '';
        let controlHTML = '';

        const filterSelect = document.getElementById('console-filter');
        const currentFilter = filterSelect ? filterSelect.value : 'all';
        let filterHTML = '<option value="all">All Workers</option>';
        let workerDropdownHTML = '<option value="all">All Workers</option>';

        Object.keys(data.workers).sort((a, b) => parseInt(a) - parseInt(b)).forEach(w_num => {
            const w = data.workers[w_num];
            const displayUsername = isStreamerMode ? '***' : w.username;
            filterHTML += `<option value="${w.worker_number}">Worker [${w.worker_number}] - ${displayUsername}</option>`;
            workerDropdownHTML += `<option value="${w.worker_number}">Worker #${w.worker_number} (${displayUsername})</option>`;

            let statusBadge = '';
            if (!w.running) statusBadge = `<span class="badge badge-danger">Stopped</span>`;
            else if (w.paused) statusBadge = `<span class="badge badge-warning">Paused</span>`;
            else if (w.sleep_mode) statusBadge = `<span class="badge badge-info">Sleeping</span>`;
            else statusBadge = `<span class="badge badge-success">Running</span>`;

            let uptimeStr = "0h 0m 0s";
            if (w.ghosty_start_time) {
                const startDt = new Date(w.ghosty_start_time);
                const now = new Date();
                const diffSec = Math.floor((now - startDt) / 1000);
                const h = Math.floor(diffSec / 3600);
                const m = Math.floor((diffSec % 3600) / 60);
                const s = diffSec % 60;
                uptimeStr = `${h}h ${m}m ${s}s`;
            }

            let runningSince = "Never";
            if (w.ghosty_start_time) {
                const startDt = new Date(w.ghosty_start_time);
                runningSince = startDt.toLocaleString();
            }

            let currentCycleDuration = "0s";
            if (w.lifetime_cycle_start_time) {
                const cycleDt = new Date(w.lifetime_cycle_start_time);
                const now = new Date();
                const diffSec = Math.floor((now - cycleDt) / 1000);
                const h = Math.floor(diffSec / 3600);
                const m = Math.floor((diffSec % 3600) / 60);
                const s = diffSec % 60;
                currentCycleDuration = `${h}h ${m}m ${s}s`;
            }

            let lastGemCheck = "Never";
            if (w.last_gem_check) {
                const gemDt = new Date(w.last_gem_check * 1000);
                lastGemCheck = gemDt.toLocaleString();
            }

            let activeQuestsText = '';
            if (w.quests && Object.keys(w.quests).length > 0) {
                activeQuestsText = Object.keys(w.quests).map(qKey => {
                    const q = w.quests[qKey];
                    return `${qKey.replace(/_/g, ' ')}: ${q.current}/${q.total}`;
                }).join(', ');
            } else {
                activeQuestsText = 'No active quests';
            }

            statusHTML += `
                <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; padding-bottom: 10px; border-bottom: 1px solid var(--border);">
                        <div>
                            <h4 style="margin: 0; font-size: 16px;">Worker #${w.worker_number}</h4>
                            <div style="font-size: 12px; color: var(--text-muted);">${displayUsername}</div>
                        </div>
                        ${statusBadge}
                    </div>
                    <div style="font-size: 13px; display: grid; grid-template-columns: 1fr; gap: 6px;">
                        <div><i class="fa-solid fa-clock" style="color: var(--text-muted); width: 16px;"></i> <strong>Running Since:</strong> ${runningSince}</div>
                        <div><i class="fa-solid fa-arrow-trend-up" style="color: var(--text-muted); width: 16px;"></i> <strong>Uptime:</strong> ${uptimeStr}</div>
                        <div><i class="fa-solid fa-terminal" style="color: var(--text-muted); width: 16px;"></i> <strong>Commands Sent:</strong> ${w.ghosty_commands_sent}</div>
                        <div><i class="fa-solid fa-gem" style="color: var(--text-muted); width: 16px;"></i> <strong>Gems Used:</strong> ${w.ghosty_gems_used}</div>
                        <div><i class="fa-solid fa-bolt" style="color: var(--text-muted); width: 16px;"></i> <strong>Speed Mode:</strong> <span class="badge" style="background:#334155;">${w.current_speed_mode}</span></div>
                        <div><i class="fa-solid fa-rotate" style="color: var(--text-muted); width: 16px;"></i> <strong>Work Cycles:</strong> ${w.lifetime_work_cycles || 0}</div>
                        <div><i class="fa-solid fa-sun" style="color: var(--text-muted); width: 16px;"></i> <strong>Day Skip Active:</strong> ${w.lifetime_day_skip_active ? "Yes" : "No"}</div>
                        <div><i class="fa-solid fa-hourglass" style="color: var(--text-muted); width: 16px;"></i> <strong>Cycle Duration:</strong> ${currentCycleDuration}</div>
                        <div><i class="fa-solid fa-bed" style="color: var(--text-muted); width: 16px;"></i> <strong>Sleeping?:</strong> ${w.sleep_mode ? "Yes" : "No"}</div>
                        <div><i class="fa-solid fa-crosshairs" style="color: var(--text-muted); width: 16px;"></i> <strong>HuntBot Active:</strong> ${w.huntbot_enabled ? "✅ Yes" : "❌ No"}</div>
                        <div><i class="fa-solid fa-brain" style="color: var(--text-muted); width: 16px;"></i> <strong>Solver Available:</strong> ${w.huntbot_solver_available ? "Yes" : "No"}</div>
                        <div><i class="fa-solid fa-recycle" style="color: var(--text-muted); width: 16px;"></i> <strong>Last Gem Check:</strong> ${lastGemCheck}</div>
                        <div style="margin-top: 5px; padding-top: 5px; border-top: 1px dashed var(--border);"><i class="fa-solid fa-list-check" style="color: var(--text-muted); width: 16px;"></i> <strong>Quests:</strong> ${activeQuestsText}</div>
                        <div style="margin-top: 5px; padding-top: 5px; border-top: 1px dashed var(--border);"><i class="fa-solid fa-ghost" style="color: var(--text-muted); width: 16px;"></i> <strong>Boss Tickets:</strong> ${w.boss_tickets}/3 ${w.is_boss_fighting ? '<span class="badge" style="background:#ef4444;">Fighting!</span>' : ''}</div>
                    </div>
                </div>
            `;

            let actionButtons = '';
            if (w.running && !w.paused) {
                actionButtons = `
                    <button class="btn btn-sm btn-warning" onclick="window.controlWorker(${w.worker_number}, 'pause')"><i class="fa-solid fa-pause"></i> Pause</button>
                    <button class="btn btn-sm btn-danger" onclick="window.controlWorker(${w.worker_number}, 'stop')"><i class="fa-solid fa-stop"></i> Stop</button>
                `;
            } else if (w.running && w.paused) {
                actionButtons = `
                    <button class="btn btn-sm btn-success" onclick="window.controlWorker(${w.worker_number}, 'resume')"><i class="fa-solid fa-play"></i> Resume</button>
                    <button class="btn btn-sm btn-danger" onclick="window.controlWorker(${w.worker_number}, 'stop')"><i class="fa-solid fa-stop"></i> Stop</button>
                `;
            } else {
                actionButtons = `<button class="btn btn-sm btn-primary" onclick="window.controlWorker(${w.worker_number}, 'start')"><i class="fa-solid fa-play"></i> Start</button>`;
            }

            controlHTML += `
                <div class="worker-control-card">
                    <div class="wcc-header">
                        <div>
                            <h4 style="margin-bottom:4px;">Worker #${w.worker_number}</h4>
                            <span class="text-muted" style="font-size:12px;">${displayUsername}</span>
                        </div>
                        ${statusBadge}
                    </div>
                    <div class="wcc-actions">
                        ${actionButtons}
                    </div>
                </div>
            `;
        });

        if (statusGrid) statusGrid.innerHTML = statusHTML;
        if (controlGrid) controlGrid.innerHTML = controlHTML;

        ['ctrl-speed-worker', 'ctrl-hb-worker', 'ctrl-pause-worker', 'ctrl-mail-worker'].forEach(id => {
            const el = document.getElementById(id);
            if (el && document.activeElement !== el) {
                const val = el.value;
                el.innerHTML = workerDropdownHTML;
                el.value = val || 'all';
            }
        });
        if (filterSelect && filterSelect.innerHTML !== filterHTML && filterHTML.length > 50) {
            filterSelect.innerHTML = filterHTML;
            filterSelect.value = currentFilter;
        }
    } catch (e) {
        console.error("Status fetch error", e);
    }
};

window.fetchLogs = async function () {
    try {
        const filterSelect = document.getElementById('console-filter');
        const filter = filterSelect ? filterSelect.value : 'all';
        let url = `${API_BASE}/logs`;
        if (filter !== 'all') url += `?worker=${filter}`;

        const res = await fetch(url);
        const logs = await res.json();
        const consoleOut = document.getElementById('console-output');

        if (logs.length > 0 && consoleOut) {
            let html = '';
            logs.forEach(log => {
                const date = new Date(log.timestamp * 1000);
                const timeStr = date.toLocaleTimeString();
                html += `<div class="log-line"><span class="log-time">[${timeStr}]</span> <span class="log-${log.level}">${log.formatted}</span></div>`;
            });
            consoleOut.innerHTML = html;
            if (isAutoScroll) {
                consoleOut.scrollTop = consoleOut.scrollHeight;
            }
        }
    } catch (e) {
        console.error("Log fetch error", e);
    }
};

window.fetchConfig = async function () {
    try {
        const res = await fetch(`${API_BASE}/config`);
        const data = await res.json();
        document.getElementById('settings-tokens').value = data.tokens;
        document.getElementById('settings-channels').value = data.channels;
    } catch (e) {
        console.error("Config fetch error", e);
    }
};

window.saveConfig = async function (type) {
    try {
        const val = document.getElementById(`settings-${type}`).value;
        const payload = {};
        payload[type] = val;

        const res = await fetch(`${API_BASE}/config`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        if (res.ok) {
            window.showToast("Saved successfully!", "success");
        }
    } catch (e) {
        window.showToast("Failed to save!", "error");
    }
};

window.restartScript = async function () {
    if (confirm("Are you sure you want to completely restart the bot script?")) {
        try {
            const res = await fetch(`${API_BASE}/restart`, { method: 'POST' });
            if (res.ok) {
                window.showToast("Restarting script! Dashboard will reconnect shortly...", "success");
                setTimeout(() => location.reload(), 3000);
            }
        } catch (e) {
            window.showToast("Failed to restart!", "error");
        }
    }
};

window.sayCommand = async function () {
    const input = document.getElementById('say-input');
    if (!input || !input.value.trim()) {
        window.showToast("Please enter text to say", "error");
        return;
    }

    try {
        const res = await fetch(`${API_BASE}/say`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text: input.value })
        });
        const data = await res.json();
        if (data.success) {
            window.showToast(`Message sent to ${data.sent} workers!`, "success");
            input.value = "";
        } else {
            window.showToast("Failed: " + data.error, "error");
        }
    } catch (e) {
        window.showToast("Error sending message", "error");
    }
};

window.fetchProfit = async function () {
    const grid = document.getElementById('profit-grid');
    if (grid) grid.innerHTML = '<i>Fetching zoo data from Discord... (This may take a few seconds)</i>';

    try {
        const res = await fetch(`${API_BASE}/profit`);
        const data = await res.json();

        if (data.success && grid) {
            let html = `<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 15px;">`;

            data.workers.forEach(w => {
                const profitColor = w.profit >= 0 ? 'var(--success)' : 'var(--danger)';
                const sign = w.profit >= 0 ? '+' : '';
                const displayUsername = isStreamerMode ? '***' : w.username;

                html += `
                    <div style="background: var(--card-bg); border: 1px solid var(--border); border-radius: 8px; padding: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
                            <h4 style="margin: 0; font-size: 16px;">Worker #${w.worker}</h4>
                            <span class="badge" style="background: #334155;">${w.status}</span>
                        </div>
                        <div style="font-size: 12px; color: var(--text-muted); margin-bottom: 10px;">${displayUsername}</div>
                        
                        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid var(--border); padding-top: 10px;">
                            <div>
                                <div style="font-size: 11px; color: var(--text-muted);">PROFIT</div>
                                <div style="font-size: 18px; font-weight: bold; color: ${profitColor};">${sign}${w.profit_str}</div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size: 11px; color: var(--text-muted);">BALANCES</div>
                                <div style="font-size: 13px;">${w.start_cash} &rarr; ${w.current_cash}</div>
                            </div>
                        </div>
                    </div>
                `;
            });

            html += `</div>`;

            const totalColor = data.total_profit >= 0 ? 'var(--success)' : 'var(--danger)';
            const totalSign = data.total_profit >= 0 ? '+' : '';

            html += `
                <div style="margin-top: 20px; background: var(--bg-color); border-left: 4px solid var(--primary); padding: 15px; border-radius: 8px; display: flex; justify-content: space-between; align-items: center;">
                    <div style="font-size: 16px; font-weight: bold;">Total Cash Profit Across All Workers</div>
                    <div style="font-size: 24px; font-weight: bold; color: ${totalColor};">${totalSign}${data.total_profit_str}</div>
                </div>
            `;

            grid.innerHTML = html;
            window.showToast("Profit fetched successfully!", "success");
        } else {
            if (grid) grid.innerHTML = `<div class="text-danger">Failed to fetch profit: ${data.error || 'Unknown error'}</div>`;
            window.showToast("Failed to fetch profit", "error");
        }
    } catch (e) {
        if (grid) grid.innerHTML = `<div class="text-danger">Error: ${e.message}</div>`;
        window.showToast("Error fetching profit", "error");
    }
};

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.nav-item').forEach(btn => {
        btn.addEventListener('click', () => {
            document.querySelectorAll('.nav-item').forEach(b => b.classList.remove('active'));
            document.querySelectorAll('.tab-pane').forEach(t => t.classList.remove('active'));

            btn.classList.add('active');
            const target = btn.getAttribute('data-target');
            const targetEl = document.getElementById(target);
            if (targetEl) targetEl.classList.add('active');

            const sidebar = document.getElementById('sidebar');
            if (window.innerWidth <= 768 && sidebar) {
                sidebar.classList.remove('open');
            }
            if (target === 'tab-settings') window.fetchConfig();
        });
    });

    const mobToggle = document.getElementById('mobile-toggle');
    const mobClose = document.getElementById('mobile-close');
    const sidebar = document.getElementById('sidebar');

    if (mobToggle) mobToggle.addEventListener('click', () => sidebar.classList.add('open'));
    if (mobClose) mobClose.addEventListener('click', () => sidebar.classList.remove('open'));

    const autoScrollToggle = document.getElementById('console-autoscroll');
    if (autoScrollToggle) {
        autoScrollToggle.addEventListener('change', (e) => {
            isAutoScroll = e.target.checked;
        });
    }

    const clearBtn = document.getElementById('console-clear');
    if (clearBtn) {
        clearBtn.addEventListener('click', () => {
            document.getElementById('console-output').innerHTML = '';
        });
    }

    const streamerModeToggle = document.getElementById('settings-streamer-mode');
    if (streamerModeToggle) {
        streamerModeToggle.checked = isStreamerMode;
        streamerModeToggle.addEventListener('change', (e) => {
            isStreamerMode = e.target.checked;
            localStorage.setItem('ghostyStreamerMode', isStreamerMode);
            window.fetchStatus();
            if (document.getElementById('tab-profit').classList.contains('active')) {
                window.fetchProfit();
            }
        });
    }

    setInterval(() => {
        window.fetchStatus();
        const tabConsole = document.getElementById('tab-console');
        if (tabConsole && tabConsole.classList.contains('active')) {
            window.fetchLogs();
        }
    }, 2000);

    window.fetchStatus();
    window.fetchLogs();
});
''',
    'dashboard/templates/index.html': r'''<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GhoSty OwO Dashboard</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}?v=1.1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @media (max-width: 992px) {

            .hide-mobile,
            .hide-mobile-title {
                display: none !important;
            }

            .header-actions {
                gap: 6px !important;
            }

            .icon-only-mobile {
                padding: 6px 8px !important;
                gap: 0 !important;
            }

            .donate-btn-mobile {
                padding: 6px 10px !important;
                gap: 4px !important;
            }
        }
    </style>
</head>

<body class="dark-mode">

    <div class="sidebar" id="sidebar">
        <div class="sidebar-header">
            <div class="brand">
                <img src="/assets/ghosty%20owo%20logo.jpeg" alt="GhoSty Logo"
                    style="width: 32px; height: 32px; border-radius: 50%; object-fit: cover;">
                <div class="brand-text">
                    <h2>GhoSty OwO</h2>
                    <span>Async Development</span>
                </div>
            </div>
            <button class="mobile-close" id="mobile-close"><i class="fa-solid fa-times"></i></button>
        </div>

        <nav class="nav-menu">
            <button class="nav-item active" data-target="tab-home">
                <i class="fa-solid fa-home"></i> Home
            </button>
            <button class="nav-item" data-target="tab-status">
                <i class="fa-solid fa-chart-pie"></i> Status
            </button>
            <button class="nav-item" data-target="tab-control">
                <i class="fa-solid fa-gamepad"></i> Control Panel
            </button>
            <button class="nav-item" data-target="tab-console">
                <i class="fa-solid fa-terminal"></i> Console
            </button>
            <button class="nav-item" data-target="tab-profit">
                <i class="fa-solid fa-coins"></i> Profit
            </button>
            <button class="nav-item" data-target="tab-settings">
                <i class="fa-solid fa-cog"></i> Settings
            </button>
            <button class="nav-item" data-target="tab-info">
                <i class="fa-solid fa-circle-info"></i> Info
            </button>
        </nav>
    </div>

    <div class="main-content">
        <header class="top-header">
            <button class="mobile-toggle" id="mobile-toggle"><i class="fa-solid fa-bars"></i></button>
            <div class="header-title hide-mobile-title">Dashboard Overview</div>
            <div class="header-actions" style="display: flex; gap: 10px;">
                <a href="https://github.com/WannaBeGhoSt" target="_blank" class="btn btn-sm icon-only-mobile"
                    style="background-color: var(--card-bg); border: 1px solid var(--border); color: var(--text); display: flex; align-items: center; gap: 6px; text-decoration: none; padding: 6px 12px; font-size: 13px; font-weight: 500;">
                    <i class="fa-brands fa-github" style="font-size: 15px;"></i> <span class="hide-mobile">GitHub</span>
                </a>
                <a href="https://discord.gg/asMJGgDA7u" target="_blank" class="btn btn-sm icon-only-mobile"
                    style="background-color: #5865F2; border: 1px solid #5865F2; color: white; display: flex; align-items: center; gap: 6px; text-decoration: none; padding: 6px 12px; font-size: 13px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                    <i class="fa-brands fa-discord" style="font-size: 15px;"></i> <span
                        class="hide-mobile">Discord</span>
                </a>
                <a href="https://donatr.ee/brutality/" target="_blank" class="btn btn-sm donate-btn-mobile"
                    style="background-color: #22c77e; border: 1px solid #22c77e; color: white; display: flex; align-items: center; gap: 6px; text-decoration: none; padding: 6px 12px; font-size: 13px; font-weight: 500; box-shadow: 0 2px 4px rgba(0,0,0,0.2);">
                    <i class="fa-solid fa-heart" style="font-size: 15px;"></i> Donate
                </a>
            </div>
        </header>

        <div class="content-wrapper">
            <!-- HOME TAB -->
            <div id="tab-home" class="tab-pane active">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-icon purple"><i class="fa-solid fa-users"></i></div>
                        <div class="stat-details">
                            <h3>Total Workers</h3>
                            <h2 id="home-total-workers">-</h2>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon green"><i class="fa-solid fa-play"></i></div>
                        <div class="stat-details">
                            <h3>Active Workers</h3>
                            <h2 id="home-active-workers">-</h2>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon yellow"><i class="fa-solid fa-coins"></i></div>
                        <div class="stat-details">
                            <h3>Total Cowoncy</h3>
                            <h2 id="home-total-cowoncy">-</h2>
                        </div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-icon cyan"><i class="fa-solid fa-flask"></i></div>
                        <div class="stat-details">
                            <h3>Total Essence</h3>
                            <h2 id="home-total-essence">-</h2>
                        </div>
                    </div>
                </div>

                <div class="card mt-4">
                    <div class="card-header">
                        <h3>Quick Actions</h3>
                    </div>
                    <div class="card-body action-buttons">
                        <button class="btn btn-primary" onclick="controlAll('start')"><i class="fa-solid fa-play"></i>
                            Start All Workers</button>
                        <button class="btn btn-success" onclick="controlAll('resume')"><i class="fa-solid fa-play"></i>
                            Resume All</button>
                        <button class="btn btn-warning" onclick="controlAll('pause')"><i class="fa-solid fa-pause"></i>
                            Pause All</button>
                        <button class="btn btn-danger" onclick="controlAll('stop')"><i class="fa-solid fa-stop"></i>
                            Stop All</button>
                        <div style="margin-top: 15px; display: flex; gap: 10px; flex-wrap: wrap;">
                            <input type="text" id="say-input" placeholder="Enter text to say..."
                                style="flex: 1; min-width: 200px; padding: 10px; border-radius: 8px; border: 1px solid var(--border); background: var(--card-bg); color: var(--text);">
                            <button class="btn btn-primary" onclick="window.sayCommand()"><i
                                    class="fa-solid fa-comment"></i> Say All</button>
                        </div>
                    </div>
                </div>
            </div>

            <div id="toast-container" style="position: fixed; bottom: 20px; right: 20px; z-index: 9999;"></div>

            <!-- STATUS TAB -->
            <div id="tab-status" class="tab-pane">
                <div class="card">
                    <div class="card-header">
                        <h3>Worker Detailed Status</h3>
                        <button class="btn btn-sm btn-outline" onclick="window.fetchStatus()"><i
                                class="fa-solid fa-sync"></i> Refresh</button>
                    </div>
                    <div class="card-body">
                        <div class="status-grid" id="status-grid"
                            style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 15px;">
                            <!-- Rendered dynamically -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- CONTROL PANEL TAB -->
            <div id="tab-control" class="tab-pane">
                <div class="card" style="margin-bottom: 20px;">
                    <div class="card-header">
                        <h3>🎮 GhoSty OwO Main Controller Settings</h3>
                    </div>
                    <div class="card-body" style="display: flex; flex-direction: column; gap: 15px;">
                        <p class="text-muted" style="margin-bottom: 0;">Apply settings to all workers or specific
                            workers instantly.</p>

                        <div
                            style="display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px;">
                            <div
                                style="background: var(--bg-color); padding: 15px; border-radius: 8px; border: 1px solid var(--border);">
                                <h4 style="margin-bottom: 10px;"><i class="fa-solid fa-bolt"
                                        style="color: #fbbf24;"></i> Change Speed Mode</h4>
                                <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                                    <select id="ctrl-speed-worker" class="form-select" style="flex: 1;">
                                        <option value="all">All Workers</option>
                                    </select>
                                    <select id="ctrl-speed-mode" class="form-select" style="flex: 1;">
                                        <option value="lifetime">Lifetime</option>
                                        <option value="humanoid">Humanoid</option>
                                        <option value="durable">Durable</option>
                                        <option value="fast">Fast</option>
                                        <option value="efficient">Efficient</option>
                                    </select>
                                </div>
                                <button class="btn btn-primary" onclick="window.applyControllerSettings('speed')"
                                    style="width: 100%;">Apply Speed</button>
                            </div>

                            <div
                                style="background: var(--bg-color); padding: 15px; border-radius: 8px; border: 1px solid var(--border);">
                                <h4 style="margin-bottom: 10px;"><i class="fa-solid fa-crosshairs"
                                        style="color: #ef4444;"></i> Toggle HuntBot</h4>
                                <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                                    <select id="ctrl-hb-worker" class="form-select" style="flex: 1;">
                                        <option value="all">All Workers</option>
                                    </select>
                                    <select id="ctrl-hb-toggle" class="form-select" style="flex: 1;">
                                        <option value="on">On</option>
                                        <option value="off">Off</option>
                                    </select>
                                </div>
                                <button class="btn btn-primary" onclick="window.applyControllerSettings('huntbot')"
                                    style="width: 100%;">Apply HuntBot</button>
                            </div>

                            <div
                                style="background: var(--bg-color); padding: 15px; border-radius: 8px; border: 1px solid var(--border);">
                                <h4 style="margin-bottom: 10px;"><i class="fa-solid fa-pause"
                                        style="color: #f59e0b;"></i> Timed Pause</h4>
                                <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                                    <select id="ctrl-pause-worker" class="form-select" style="flex: 1;">
                                        <option value="all">All Workers</option>
                                    </select>
                                    <input type="text" id="ctrl-pause-time" placeholder="e.g. 30m, 1h30m"
                                        class="form-select" style="flex: 1; padding: 8px;">
                                </div>
                                <button class="btn btn-warning" onclick="window.applyControllerSettings('pause_time')"
                                    style="width: 100%;">Apply Timed Pause</button>
                            </div>

                            <div
                                style="background: var(--bg-color); padding: 15px; border-radius: 8px; border: 1px solid var(--border);">
                                <h4 style="margin-bottom: 10px;"><i class="fa-solid fa-envelope"
                                        style="color: #6366f1;"></i> Check Mail</h4>
                                <div style="display: flex; gap: 10px; margin-bottom: 10px;">
                                    <select id="ctrl-mail-worker" class="form-select" style="flex: 1;">
                                        <option value="all">All Workers</option>
                                    </select>
                                </div>
                                <button class="btn btn-primary" onclick="window.applyControllerSettings('mail')"
                                    style="width: 100%;">Check Mail</button>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3>Individual Worker Controls</h3>
                    </div>
                    <div class="card-body">
                        <div class="control-grid" id="control-grid">
                            <!-- Rendered dynamically -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- CONSOLE TAB -->
            <div id="tab-console" class="tab-pane">
                <div class="card console-card">
                    <div class="card-header console-header">
                        <h3>Live Console</h3>
                        <div class="console-controls">
                            <select id="console-filter" class="form-select">
                                <option value="all">All Workers</option>
                            </select>
                            <button class="btn btn-sm btn-outline" id="console-clear"><i class="fa-solid fa-eraser"></i>
                                Clear</button>
                            <label class="toggle-switch">
                                <input type="checkbox" id="console-autoscroll" checked>
                                <span class="slider"></span>
                                <span class="toggle-label">Auto-scroll</span>
                            </label>
                        </div>
                    </div>
                    <div class="card-body console-body" id="console-output">
                        <!-- Rendered dynamically -->
                    </div>
                </div>
            </div>

            <!-- PROFIT TAB -->
            <div id="tab-profit" class="tab-pane">
                <div class="card">
                    <div class="card-header">
                        <h3>Live Profit Calculator</h3>
                        <button class="btn btn-primary" onclick="fetchProfit()"><i class="fa-solid fa-calculator"></i>
                            Fetch Live Profit</button>
                    </div>
                    <div class="card-body">
                        <p class="text-muted mb-4">Clicking the button above will trigger the Zoo Profit calculator
                            logic internally to update current holdings for each worker. (Note: May trigger discord API
                            calls).</p>

                        <div class="profit-grid" id="profit-grid">
                            <!-- Rendered dynamically -->
                        </div>
                    </div>
                </div>
            </div>

            <!-- SETTINGS TAB -->
            <div id="tab-settings" class="tab-pane">
                <div class="card" style="margin-bottom: 20px;">
                    <div class="card-header">
                        <h3>Dashboard Display Settings</h3>
                    </div>
                    <div class="card-body">
                        <div
                            style="display: flex; justify-content: space-between; align-items: center; background: var(--bg-color); padding: 15px; border-radius: 8px; border: 1px solid var(--border);">
                            <div>
                                <h4 style="margin: 0; margin-bottom: 5px;"><i class="fa-solid fa-video"
                                        style="color: #a855f7;"></i> Streamer Mode</h4>
                                <div style="font-size: 13px; color: var(--text-muted);">Completely hide worker usernames
                                    and sensitive information across the dashboard.</div>
                            </div>
                            <label class="toggle-switch">
                                <input type="checkbox" id="settings-streamer-mode">
                                <span class="slider"></span>
                            </label>
                        </div>
                    </div>
                </div>

                <div class="grid-2">
                    <div class="card">
                        <div class="card-header">
                            <h3>tokens.txt</h3>
                        </div>
                        <div class="card-body">
                            <textarea id="settings-tokens" class="form-textarea" rows="10"
                                placeholder="Enter tokens here..."></textarea>
                            <button class="btn btn-primary mt-3" onclick="saveConfig('tokens')"><i
                                    class="fa-solid fa-save"></i> Save Tokens</button>
                        </div>
                    </div>
                    <div class="card">
                        <div class="card-header">
                            <h3>channels.txt</h3>
                        </div>
                        <div class="card-body">
                            <textarea id="settings-channels" class="form-textarea" rows="10"
                                placeholder="Enter channel IDs here..."></textarea>
                            <button class="btn btn-primary mt-3" onclick="saveConfig('channels')"><i
                                    class="fa-solid fa-save"></i> Save Channels</button>
                        </div>
                    </div>
                </div>

                <div class="card mt-4 danger-zone">
                    <div class="card-header">
                        <h3 class="text-danger"><i class="fa-solid fa-triangle-exclamation"></i> Danger Zone</h3>
                    </div>
                    <div class="card-body">
                        <p>Restarting the script will temporarily disconnect all workers and reboot the entire Python
                            process.</p>
                        <button class="btn btn-danger mt-2" onclick="restartScript()"><i
                                class="fa-solid fa-power-off"></i> Restart Script</button>
                    </div>
                </div>
            </div>
            
            <!-- INFO TAB -->
            <div id="tab-info" class="tab-pane">
                <div class="card" style="margin-bottom: 20px;">
                    <div class="card-header">
                        <h3><i class="fa-solid fa-code-branch"></i> Version Info</h3>
                    </div>
                    <div class="card-body">
                        <h4 style="color: #a855f7; margin-bottom: 5px;">GhoSty OwO V4 Alpha Build</h4>
                        <strong>Stable Alpha Build Version: 280826.4.1.0</strong>
                        <p style="color: var(--text-muted); font-size: 14px; margin-top: 15px;">
                            <strong>What's New:</strong>
                            <ul style="color: var(--text-muted); font-size: 14px; margin-top: 10px; line-height: 1.6;">
                                <li><strong>Built-in Web Dashboard:</strong> Real-time monitoring, live stats, and remote control of all workers natively integrated.</li>
                                <li><strong>Boss Module:</strong> Automated and intelligent boss fighting support.</li>
                                <li><strong>Quests Module:</strong> Fully automated quest tracking, updating, and claiming.</li>
                                <li><strong>Mail Module:</strong> Automatically fetches and claims mails.</li>
                                <li><strong>Humanoid Speed Mode:</strong> Advanced dynamic fatigue algorithm using a bezier curve-shaped gaussian distribution combined with random server lurking to seamlessly evade detection.</li>
                                <li><strong>Revamped UI Engine:</strong> A completely redesigned CLI backend interface structure for optimal display.</li>
                                <li><strong>Codebase Rewrite:</strong> Codebase rewrite from discord.py to discord.py-self.</li>
                            </ul>
                        </p>
                    </div>
                </div>

                <div class="card">
                    <div class="card-header">
                        <h3><i class="fa-solid fa-laptop-code"></i> About Developer</h3>
                    </div>
                    <div class="card-body" style="display: flex; align-items: center; gap: 20px;">
                        <img src="/assets/brutality.jpg" alt="Brutality Logo" style="width: 80px; height: 80px; border-radius: 50%; object-fit: cover; box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
                        <div>
                            <p style="color: var(--text-muted); font-size: 15px; line-height: 1.6; margin: 0;">
                                <strong>Made With ♥ By @WannaBeGhoSt (GitHub)</strong><br>
                                This script is continuously developed and maintained by <strong>GhoSty | Brutality (🇮🇳 Async Development)</strong>. We focus on building advanced, highly optimized, and robust automation tools for the community.
                            </p>
                            <div style="margin-top: 15px; display: flex; gap: 10px;">
                                <a href="https://discord.gg/asMJGgDA7u" target="_blank" class="btn btn-primary" style="background-color: #5865F2; border: none;"><i class="fa-brands fa-discord"></i> Join Discord</a>
                                <a href="https://github.com/WannaBeGhoSt" target="_blank" class="btn btn-primary" style="background-color: #24292e; border: none;"><i class="fa-brands fa-github"></i> GitHub</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>
    </div>

    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
</body>

</html>''',
}

_EMBEDDED_BIN = {
    'assets/brutality.jpg': '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',
    'assets/cli view.png': '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',
    'assets/ghosty owo logo.jpeg': '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',
    'assets/web dashboard.png': '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',
    'core/letters/0/a.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUi6eLo4hGqLJJbP+/rdn7mzodPma8DQlM0nlmlpK/oR04U2cR255TfMFijiWXdoX4jaHsfkN76acJBczxpthNTmbcpS8hRlc4vhbT+Y0JgPNY/B09XNZ55TQBAD4PSjx',
    'core/letters/0/b.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtFALMTBBiQbskOMgJS1p4tjiIZocsmsv//tmUXeeKemtGz8eNHnh0rhSd4i354TjI2n+V88+vJZmHvT1R+POG9Kfym+V7Alc8JyDgabBN5bTxZ76QKNYfB09XNZ55TQBACyAyif',
    'core/letters/0/d.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtFALMTBBiQbskOMgJSlp4tjiIZocoqCkMXZf//ll03hPKbQKvdklsREW481+188VxdLUX/rnZri8kx588S9jvbPed1ns1V2MTBMdePZ+luJvQxoCIOnq5/LOqeEJgCRUyJ+',
    'core/letters/0/e.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUvaeLo4hGqLJJbP+/rdn7mzodPma8DQlM8lxW2a8lrKykfzM3je8m3KSXMwYb6bU5GzKUfIWvsjY+CZmU47UE0ZGBvmbvJcs5z0MBxrF4Onq57LOKaEJAOhSJj0=',
    'core/letters/0/g.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUu6eLo4hGqLJJbP+/rdn7mzodPma8DQlM8lxW2a8lrKykbz47KLZCWrCXDKbcpS8hb0cDsxp13WYMNdnmm/PCbUDOUouk1OFI2cxvJ3He7UyND4XaCSDp6ufyzqnhCYA5fIoLA==',
    'core/letters/0/k.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtI8IDYHG5Ccq9nvBKSyPF0cQzREWyde5D2gwOHi7f5ab+6q3SWmZ1X3Ptvh8MF9yveGjJjzUce337Nu2vj+iZ9/SPqhE71NhxY/MHDLsw4puL2w2ftgosOuSx7CPIacUZ7JuiFcFbz/XbwONohaT/h5BShX9517XoLrdDOTKsPzE8qvfQDayuDp6ueyzimhCQCH/z4W',
    'core/letters/0/m.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUgaeLo4hGqLJJbP+/rdn7mzodPma8HRK9q3pp05wHDqxLVl48R21FOkPG91zm9r4/jIxMVx+wt559IjBU6BeBk9XP5d1TglNAEslJDg=',
    'core/letters/0/p.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtFALMTBBiQbskOMgJSTp4tjiIZocsmsv//tmTsbOl2+JjxNyUxy3JYZr6WsbCQ/s/cN76YcqassvH5uTxa48CXV5PxqlbuoyXRz55diub85TAzzRbiZwvym6QBNY/B09XNZ55TQBADyQSWv',
    'core/letters/0/q.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtFALMTBBiQbskOMgJSvp4tjiIZocsmsv//tmTsbOl2+JjxNyUxy3JYZr6WsbCQ/s/cN76YcqassvH5uTxa48CXV5Pxqlbsm0vAmJWdli85zwS2cYgonzCalCkfOYnBmFrwZ4Tx9P9BgBk9XP5d1TglNANKjKpw=',
    'core/letters/0/s.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUiaeLo4hGqLJJbP+/rdn7mzodPma8DQlM8lxW2a8lrKykbz4bJ3ZEuzlDgJPCwMaFKqTLdhYGNjP8qxSaC9QAOpn8HT1c1nnlNAEAOPmHjw=',
    'core/letters/0/t.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUrqeLo4hGqLJJbP+/rdn7mzodPma8DQlM+lImvCmyd+XGiWtUDy9LND3wgK5J4yMDKt3s315bXjfFKiRwdPVz2WdU0ITAK6iIb0=',
    'core/letters/0/v.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtI8IDYHG5Ccq9nvBKTKPV0cQzREWycw8jUo8DBLfkz9dzT8p/i+titLlkjr6BiafLu1cGnPzvv3PjqkO9/XYNh2PEc8YJnWgrZ94bGbw5yimK7lMixpyBL703hZ7ECKntrXO6aXy+tVmW/2XfjEm3PKbztjwJ1Fbz9M5xVkWLKZ5YpNq7r0etNeRbt4Zv2mT833FYFOYPB09XNZ55TQBAAZQUF5',
    'core/letters/0/w.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUrqeLo4hGqLJJbP+/rdnFnnjnZrCYsjZaXjQZIJTf1ZT2zUFfg63JzfUzZpePldnUFzPe/7mm4J6oEYGT1c/l3VOCU0AKxMfCQ==',
    'core/letters/0/x.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtI8IDYHG5Ccq9nvBKSaPF0cQzREp07q5m1Q4HHpXvxSK2/pagvpqiPpp1h9VQ5Ou8cuJb312oztr6uPruddrtFZLZst8klmuq3cuS9sAedTrqqVn22Zk3whr0BwgfvHLqnUXpmDBm9ZmGJZBB/+Xxa4y7j0aM9W6SLGRfasft8fu6V0JMTya+3aPP/2nwybGVO3VzLZM3Y3VXiKCXzyArqGwdPVz2WdU0ITAJw/RPs=',
    'core/letters/0/y.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtFALMTBBiQbskOMgJSdp4tjiIZocsmsv//tmUXeeKemtGy8mJlS6vNi0pEP7qaOzpkT2FmUi3yEhTcqmH75LHyNpetNSk7njLpzi+f7MqwL4L2xUfCJF9AkBk9XP5d1TglNAI47Joo=',
    'core/letters/0/z.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUv6eLo4hGqLJJbP+/rdn7mzodPma8DQlM0klRXjX5+9LjYweXW3xZT4hNGdWQeaBlZzz2dbM4sg8cMGlh03E90hWQ7bTdYZJB9glPK8yGPWsEWFksKpXWVSzR/QU0GgGT1c/l3VOCU0AQHgueA==',
    'core/letters/1/f.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUoaeLo4hGqLJJbP+/rdn7mzodPma8DQlM8lxW2a8lrKykbz4bJ3ZEu7MTELzUlrl/powMnxezyEb0N7JB9TM4Onq57LOKaEJAImkHa4=',
    'core/letters/1/h.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtFALMTBBiQbskOMgJStp4tjiIZocsmsv//tmUXeeKemtGz8eNHnh0rhSd4i354TjI2n+V88+vJZmHvT1R+POG9Kfym+t8L3wo+F8Q4MDPW+3AzJuj76QIMYPF39XNY5JTQBAPtDKDM=',
    'core/letters/1/o.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUuaeLo4hGqLJJbP+/rdn7mzodPma8DQlM8lxW2a8lrKykfzM3je8m3KkrrLw+rk9WeDCl1ST86tVjsHnDOfFz47zjgGNYPB09XNZ55TQBAC8RiPR',
    'core/letters/2/c.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUnqeLo4hGqLJJbP+/rdn7mzodPma8DQlM8lxW2a8lrKykbz4bJ3ZbqaOzZMLC5ZzMNzdyvZtvaPQfaBOBk9XP5d1TglNAF8OHvo=',
    'core/letters/2/n.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUvqeLo4hGqLJJbP+/rdn7mzodPma8DQlM8lxW2a8lrKykfzM3je8m3KkrrLwnnOUE2Do38n2PZrh2kGgVgZPVz+XdU4JTQCKCx9i',
    'core/letters/2/r.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUrqeLo4hGqLJJbP+/rdn7mzodPma8DQlM8lxW2a8lrKykbz4bJ3ZbqaOzcUT2FkYFDayyIRFV20AamTwdPVzWeeU0AQAEHccQQ==',
    'core/letters/2/u.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUoaeLo4hGqLJJbP+/rdnFnnjnZrSsvFiZkqpz4tJRz64mzo6Z05gZ1Eu8hEW3qhg+uWzMMORY5zn13yqMAdqZvB09XNZ55TQBADyfSGE',
    'core/letters/3/j.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUuaeLo4hGqLJKQpCFmf//ZdfNoXzmEKr3FUWXt1NTE2sln++LzUyEhL+knLzSEeOsOG2hisTUoUjZzGo1XFeXPb9xDagEQyern4u65wSmgCHhCOk',
    'core/letters/3/l.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtEgzMEGJIteP6kBUvqeLo4hGqLJJbP+/rdnFnnjnZrSsvHjRZ8fKoUne7Oa2s4o8HO4PRFp1Da6ePTlc3WG/tlsX+Q5pQ4CtTJ4uvq5rHNKaAIA2lAhcQ==',
    'core/letters/4/i.png': 'eNrrDPBz5+WS4mJgYOD19HAJAtKcIDYHG5CsZnABUUqeLo4hEpLJKQ5Mfpv//28v/L7UyOjQDR8DNruqEMHDCTxMDGG/WaT+rataDFTN4Onq57LOKaEJAGjAF9A=',
}


# ---------------------------------------------------------------------------
# LOGGING
# ---------------------------------------------------------------------------

def log_info(msg):
    print(f"[INFO] {msg}")

def log_warn(msg):
    print(f"[WARN] {msg}")

def log_error(msg):
    print(f"[ERROR] {msg}")

def log_success(msg):
    print(f"[✓] {msg}")

def log_worker_start(user_id, worker_num, token_short, channel_id):
    print(f"[USER {user_id}] [W#{worker_num}] Starting with token {token_short}... in channel {channel_id}")

def log_worker_ready(user_id, worker_num, username, channel_id):
    print(f"[USER {user_id}] [W#{worker_num}] Ready: {username} farming in {channel_id}")

def log_controller_ready(username):
    print(f"[CONTROLLER] Ready: {username} | Command: .panel (public multi-user)")

# ---------------------------------------------------------------------------
# USER STATE MANAGEMENT
# ---------------------------------------------------------------------------

class UserWorker:
    """Single worker for a user."""
    def __init__(self, worker_num: int, token: str, channel_id: int):
        self.worker_num = worker_num
        self.token = token
        self.channel_id = channel_id
        self.is_valid = True
        self.username = None
        self.bot = None
        self.running = False
        self.created_at = datetime.now()
    
    def mark_invalid(self):
        self.is_valid = False
        self.running = False
    
    def __repr__(self):
        status = "✅ Valid" if self.is_valid else "❌ Invalid"
        return f"W#{self.worker_num}: {self.username or 'Connecting'} → CH {self.channel_id} [{status}]"


class UserConfig:
    """Configuration for a single Discord user."""
    def __init__(self, user_id: int, username: str):
        self.user_id = user_id
        self.username = username
        self.workers: Dict[int, UserWorker] = {}  # worker_num -> UserWorker
        self.next_worker_num = 1
        self.created_at = datetime.now()
    
    def add_worker(self, token: str, channel_id: int) -> UserWorker:
        """Add a new worker, return the worker object."""
        worker = UserWorker(self.next_worker_num, token, channel_id)
        self.workers[self.next_worker_num] = worker
        self.next_worker_num += 1
        return worker
    
    def get_valid_workers(self) -> List[UserWorker]:
        """Get only valid workers."""
        return [w for w in self.workers.values() if w.is_valid]
    
    def get_all_workers(self) -> List[UserWorker]:
        """Get all workers (valid and invalid)."""
        return list(self.workers.values())
    
    def remove_invalid_workers(self):
        """Remove invalid workers from config."""
        to_remove = [num for num, w in self.workers.items() if not w.is_valid]
        for num in to_remove:
            del self.workers[num]


class UserManager:
    """Manage all user configurations."""
    def __init__(self):
        self.users: Dict[int, UserConfig] = {}  # user_id -> UserConfig
        self.lock = threading.Lock()
    
    def get_or_create_user(self, user_id: int, username: str) -> UserConfig:
        """Get existing user or create new one."""
        with self.lock:
            if user_id not in self.users:
                self.users[user_id] = UserConfig(user_id, username)
            return self.users[user_id]
    
    def get_user(self, user_id: int) -> Optional[UserConfig]:
        """Get user config if exists."""
        with self.lock:
            return self.users.get(user_id)

user_manager = UserManager()

# ---------------------------------------------------------------------------
# TOKEN & CHANNEL VALIDATION
# ---------------------------------------------------------------------------

def _parse_token_channel_pairs(input_string: str) -> Optional[List[Tuple[str, int]]]:
    """
    Parse input: TOKEN1-CHANNELID1,TOKEN2-CHANNELID2
    Returns list of (token, channel_id) tuples or None if invalid
    """
    if not input_string or not input_string.strip():
        return None
    
    pairs = []
    for pair_str in input_string.split(","):
        pair_str = pair_str.strip()
        if not pair_str:
            continue
        
        parts = pair_str.split("-")
        if len(parts) != 2:
            return None  # Invalid format
        
        token = parts[0].strip()
        channel_str = parts[1].strip()
        
        if not token or len(token) < 50:  # Discord tokens are long
            return None
        
        if not channel_str.isdigit():
            return None
        
        channel_id = int(channel_str)
        pairs.append((token, channel_id))
    
    return pairs if pairs else None


def _validate_token_format(token: str) -> bool:
    """Quick token format validation."""
    return len(token) > 50 and "." in token


def _validate_channel_id(channel_id: int) -> bool:
    """Quick channel ID validation."""
    return isinstance(channel_id, int) and channel_id > 0

# Configuration
RETRY_DELAY_INITIAL = 5
RETRY_DELAY_FACTOR = 1.5
RETRY_DELAY_MAX = 120

main_token = brutality_ghosty.environ.get("DISCORD_BOT_TOKEN", "").strip()

if not main_token:
    log_error("DISCORD_BOT_TOKEN is required!")
    sys.exit(1)

web_dashboard_enabled = brutality_ghosty.environ.get("WEB_DASHBOARD", "true").strip().lower() not in ("0", "false", "no", "off")

print(f"""
╔════════════════════════════════════════════════════════════════╗
║          GhoSty OwO V4 — Public Multi-User Edition             ║
║                                                                 ║
║  Configuration: Via .panel command (per-user)                  ║
║  Format: TOKEN1-CHANNELID1,TOKEN2-CHANNELID2                  ║
║  Users: Isolated, real-time validation                         ║
║  Status: 🟢 READY (awaiting user configuration)                ║
╚════════════════════════════════════════════════════════════════╝
""")

_materialize_embedded_files()

from core.utils import create_bot
from core.heart import WorkerState, WorkerManager, register_commands, _run_farming_loop, PseudoCtx

# Global worker manager for farm operations
global_manager = WorkerManager()
global_manager.set_has_channels_config(True)

# ---------------------------------------------------------------------------
# WORKER THREAD (Per-User)
# ---------------------------------------------------------------------------

def run_user_worker(user_id: int, user_config: UserConfig, user_worker: UserWorker):
    """Run a single worker for a specific user."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    label = f"[USER {user_id}] [W#{user_worker.worker_num}]"
    retry_delay = RETRY_DELAY_INITIAL
    attempt = 0

    while user_worker.is_valid:
        attempt += 1
        if attempt > 1:
            log_info(f"{label} Reconnecting in {retry_delay}s...")
            _time.sleep(retry_delay)
            retry_delay = min(retry_delay * RETRY_DELAY_FACTOR, RETRY_DELAY_MAX)

        try:
            bot = create_bot(user_worker.worker_num)
            user_worker.bot = bot

            ws = WorkerState(user_worker.worker_num)
            ws.bot = bot
            ws.auto_start_channel_id = user_worker.channel_id
            ws.current_speed_mode = "efficient"
            ws.huntbot_enabled = True
            
            global_manager.register_worker(ws)
            register_commands(bot, ws)

            @bot.event
            async def on_ready():
                user_worker.username = str(bot.user)
                user_worker.running = True
                log_worker_ready(user_id, user_worker.worker_num, str(bot.user), user_worker.channel_id)
                
                # Auto-start farming
                if user_worker.channel_id and user_worker.is_valid:
                    ch_id = user_worker.channel_id
                    success, blocking = global_manager.try_claim_channel(ch_id, user_worker.worker_num)
                    
                    if success:
                        target_channel = bot.get_channel(ch_id)
                        if target_channel:
                            pseudo_ctx = PseudoCtx(target_channel, bot)
                            asyncio.create_task(_run_farming_loop(pseudo_ctx, ws, bot))
                            log_info(f"{label} Auto-started farming in channel {ch_id}")
                    else:
                        log_warn(f"{label} Channel {ch_id} locked by another worker")

            @bot.event
            async def on_disconnect():
                log_info(f"{label} Disconnected")

            @bot.event
            async def on_error(event, *args, **kwargs):
                import traceback
                log_error(f"{label} {event}")
                traceback.print_exc()

            log_worker_start(user_id, user_worker.worker_num, user_worker.token[:20], user_worker.channel_id)
            bot.run(user_worker.token, log_handler=None)
            break

        except Exception as e:
            log_error(f"{label} {str(e)}")
            user_worker.mark_invalid()

    loop.close()

# ---------------------------------------------------------------------------
# DISCORD BOT UI
# ---------------------------------------------------------------------------

import discord
from discord.ext import commands

class AddWorkersModal(discord.ui.Modal, title="Add Worker Tokens & Channels"):
    """Modal for entering TOKEN-CHANNELID pairs."""
    
    workers_input = discord.ui.TextInput(
        label="Token-Channel Pairs",
        placeholder="Format: TOKEN1-CHANNELID1,TOKEN2-CHANNELID2",
        style=discord.TextStyle.long,
        min_length=50,
        max_length=3000,
        required=True
    )
    
    def __init__(self, user_id: int, user_config: UserConfig, discord_user: discord.User):
        super().__init__()
        self.user_id = user_id
        self.user_config = user_config
        self.discord_user = discord_user
    
    async def on_submit(self, interaction: discord.Interaction):
        """Process worker submission."""
        input_text = str(self.workers_input).strip()
        
        # Parse input
        pairs = _parse_token_channel_pairs(input_text)
        
        if not pairs:
            await interaction.response.send_message(
                "❌ **Invalid Format**\n\n"
                "Expected: `TOKEN1-CHANNELID1,TOKEN2-CHANNELID2`\n"
                "Make sure:\n"
                "• Tokens and channel IDs are separated by `-` (hyphen)\n"
                "• Multiple pairs are separated by `,` (comma)\n"
                "• Tokens are valid Discord user tokens\n"
                "• Channel IDs are valid 18-digit numbers",
                ephemeral=True
            )
            return
        
        # Validate each pair
        errors = []
        valid_pairs = []
        
        for i, (token, channel_id) in enumerate(pairs, 1):
            if not _validate_token_format(token):
                errors.append(f"Pair {i}: Token format invalid")
                continue
            
            if not _validate_channel_id(channel_id):
                errors.append(f"Pair {i}: Channel ID invalid")
                continue
            
            valid_pairs.append((token, channel_id))
        
        if errors:
            error_msg = "❌ **Validation Errors**\n\n" + "\n".join(errors)
            await interaction.response.send_message(error_msg, ephemeral=True)
            return
        
        if not valid_pairs:
            await interaction.response.send_message(
                "❌ No valid pairs found!",
                ephemeral=True
            )
            return
        
        # Add workers
        added = 0
        for token, channel_id in valid_pairs:
            user_worker = self.user_config.add_worker(token, channel_id)
            
            # Start worker thread
            t = threading.Thread(
                target=run_user_worker,
                args=(self.user_id, self.user_config, user_worker),
                daemon=True,
                name=f"User-{self.user_id}-Worker-{user_worker.worker_num}"
            )
            t.start()
            added += 1
        
        await interaction.response.send_message(
            f"✅ **Added {added} worker(s)**\n\n"
            f"Workers are starting and will begin farming automatically.\n"
            f"Run `.panel` again to check status.",
            ephemeral=True
        )


class PanelView(discord.ui.View):
    """Panel view with Add Workers button."""
    
    def __init__(self, user_id: int, user_config: UserConfig, discord_user: discord.User):
        super().__init__()
        self.user_id = user_id
        self.user_config = user_config
        self.discord_user = discord_user
    
    @discord.ui.button(label="➕ Add Workers", style=discord.ButtonStyle.blurple)
    async def btn_add_workers(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Open modal to add workers (only for panel owner)."""
        
        # Check if button clicker is the panel owner
        if interaction.user.id != self.user_id:
            await interaction.response.send_message(
                "❌ You can only manage your own workers.\n"
                "Run `.panel` to create your own panel.",
                ephemeral=True
            )
            return
        
        modal = AddWorkersModal(self.user_id, self.user_config, self.discord_user)
        await interaction.response.send_modal(modal)


class ControllerBot(commands.Cog):
    """Main controller with .panel command."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="panel")
    async def cmd_panel(self, ctx):
        """Display user's configuration panel."""
        
        user_id = ctx.author.id
        username = ctx.author.name
        
        # Get or create user config
        user_config = user_manager.get_or_create_user(user_id, username)
        
        # Build panel embed
        valid_workers = user_config.get_valid_workers()
        
        embed = discord.Embed(
            title="🎮 GhoSty OwO — Your Worker Panel",
            description=(
                "**⚠️ Token Security**\n"
                "Only you can manage your workers.\n"
                "Tokens are stored securely and never shared."
            ),
            color=discord.Color.blurple()
        )
        
        # Current workers section
        if valid_workers:
            worker_lines = []
            for w in valid_workers:
                username_str = w.username if w.username else "🔄 Connecting..."
                worker_lines.append(
                    f"**Worker #{w.worker_num}** — {username_str}\n"
                    f"└─ Channel: <#{w.channel_id}> | Status: ✅ Valid"
                )
            
            embed.add_field(
                name=f"📊 Your Workers ({len(valid_workers)})",
                value="\n\n".join(worker_lines),
                inline=False
            )
        else:
            embed.add_field(
                name="📊 Your Workers",
                value="🟡 No workers configured yet.\n\nClick **Add Workers** below to start!",
                inline=False
            )
        
        # Instructions
        embed.add_field(
            name="📝 How to Add Workers",
            value=(
                "1. Click **Add Workers** button below\n"
                "2. Enter token-channel pairs in format:\n"
                "   `TOKEN1-CHANNELID1,TOKEN2-CHANNELID2`\n"
                "3. Each worker starts farming automatically\n"
                "4. Run `.panel` anytime to check status or add more"
            ),
            inline=False
        )
        
        # Settings
        embed.add_field(
            name="⚙️ Auto Settings",
            value="Speed: **Efficient** 🐢 | HuntBot: **Enabled** 🎯",
            inline=False
        )
        
        embed.set_footer(text=f"User: {username} | Run .panel anytime to update")
        
        # Send panel with button
        view = PanelView(user_id, user_config, ctx.author)
        await ctx.send(embed=embed, view=view)


async def setup_controller_bot():
    """Initialize the main controller bot."""
    intents = discord.Intents.default()
    intents.message_content = True
    intents.guilds = True
    
    bot = commands.Bot(command_prefix=".", intents=intents, help_command=None)
    
    @bot.event
    async def on_ready():
        log_controller_ready(str(bot.user))
    
    await bot.add_cog(ControllerBot(bot))
    return bot


def run_main_controller(token):
    """Run the main controller bot."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    label = "[MAIN-CTRL]"
    retry_delay = RETRY_DELAY_INITIAL
    attempt = 0

    while True:
        attempt += 1
        if attempt > 1:
            log_info(f"{label} Reconnecting in {retry_delay}s (attempt {attempt})...")
            _time.sleep(retry_delay)
            retry_delay = min(retry_delay * RETRY_DELAY_FACTOR, RETRY_DELAY_MAX)

        try:
            bot = loop.run_until_complete(setup_controller_bot())

            @bot.event
            async def on_disconnect():
                log_info(f"{label} Disconnected")

            @bot.event
            async def on_resumed():
                log_info(f"{label} Resumed")

            log_info(f"{label} Starting...")
            bot.run(token, log_handler=None)
            break

        except Exception as e:
            log_error(f"{label} {str(e)}")

    loop.close()

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    threads = []

    # Dashboard
    if web_dashboard_enabled:
        try:
            from dashboard.app import start_server
            dash_t = threading.Thread(target=start_server, daemon=True, name="Dashboard")
            dash_t.start()
            threads.append(dash_t)
            log_success("Dashboard started")
        except Exception as e:
            log_warn(f"Dashboard: {e}")

    # Main controller
    if main_token:
        t = threading.Thread(
            target=run_main_controller,
            args=(main_token,),
            daemon=True,
            name="MainController"
        )
        t.start()
        threads.append(t)
        log_success("Controller thread started")

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        log_info("Shutdown")
        sys.exit(0)
