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

_EMBEDDED_TEXT = {}
_EMBEDDED_BIN = {}

# ---------------------------------------------------------------------------
# LOGGING & UI
# ---------------------------------------------------------------------------

def clear_screen():
    brutality_ghosty.system('cls' if brutality_ghosty.name == 'nt' else 'clear')

def log_info(msg):
    print(f"[INFO] {msg}")

def log_warn(msg):
    print(f"[WARN] {msg}")

def log_error(msg):
    print(f"[ERROR] {msg}")

def log_success(msg):
    print(f"[✓] {msg}")

def log_worker_start(number):
    print(f"[WORKER #{number:02d}] Starting...")

def log_worker_ready(number, username, auto_start_ch):
    ch_str = f"(channel: {auto_start_ch})" if auto_start_ch else "(waiting for channel)"
    print(f"[WORKER #{number:02d}] Ready: {username} {ch_str}")

def log_controller_ready(username):
    print(f"[CONTROLLER] Ready: {username} | Command: .panel")

def log_disconnect(label):
    print(f"{label} DISCONNECTED")

def log_resumed(label):
    print(f"{label} RESUMED")

def log_event_error(label, event):
    print(f"{label} EVENT ERROR: {event}")

def log_retry(label, delay, attempt):
    print(f"{label} Reconnecting in {delay}s (attempt {attempt})...")

def log_fatal_error(label, exc):
    print(f"{label} FATAL: {exc}")

def log_net_error(label, exc):
    print(f"{label} Network error: {exc}")

def log_shutdown():
    print("[SHUTDOWN] Graceful shutdown.")

# ---------------------------------------------------------------------------
# CONFIGURATION - RUNTIME (In-Memory)
# ---------------------------------------------------------------------------

# Global state for modal panel
class ConfigState:
    def __init__(self):
        self.worker_tokens = []      # List of token strings
        self.channel_ids = []        # List of channel IDs (ints)
        self.is_configured = False   # Both tokens and channels set

config_state = ConfigState()

RETRY_DELAY_INITIAL = 5
RETRY_DELAY_FACTOR = 1.5
RETRY_DELAY_MAX = 120

# Parse environment
main_token = brutality_ghosty.environ.get("DISCORD_BOT_TOKEN", "").strip()

if not main_token:
    log_error("DISCORD_BOT_TOKEN is required! Set it and restart.")
    sys.exit(1)

web_dashboard_enabled = brutality_ghosty.environ.get("WEB_DASHBOARD", "true").strip().lower() not in ("0", "false", "no", "off")

clear_screen()

print(f"""
╔════════════════════════════════════════════════════════════════╗
║          GhoSty OwO V4 — Modal Panel Edition                   ║
║                                                                 ║
║  Configuration: Via .panel command in Discord                  ║
║  Workers: Waiting for token & channel setup                    ║
║  Status: 🟡 READY (awaiting configuration)                     ║
╚════════════════════════════════════════════════════════════════╝
""")

# Materialize embedded files
_materialize_embedded_files()

# Import core modules
from core.utils import create_bot
from core.heart import WorkerState, WorkerManager, register_commands, _run_farming_loop, PseudoCtx

manager = WorkerManager()
manager.set_has_channels_config(False)  # Will be set to True when configured


# ---------------------------------------------------------------------------
# UTILITY FUNCTIONS
# ---------------------------------------------------------------------------

def _parse_channel_id(line):
    """Parse a channel ID from various formats."""
    line = line.strip()
    if not line or line.startswith("#"):
        return None
    if line.isdigit():
        return int(line)
    match = re.search(r'/channels/\d+/(\d+)', line)
    if match:
        return int(match.group(1))
    return None

def _validate_tokens(token_string):
    """Parse and validate comma-separated tokens. Returns list or None."""
    tokens = [t.strip() for t in token_string.split(",")]
    tokens = [t for t in tokens if t]
    if not tokens:
        return None
    return tokens

def _validate_channels(channel_string):
    """Parse and validate comma-separated channel IDs. Returns list or None."""
    parts = [p.strip() for p in channel_string.split(",")]
    channels = []
    for part in parts:
        ch_id = _parse_channel_id(part)
        if ch_id is not None:
            channels.append(ch_id)
    if not channels:
        return None
    return channels


# ---------------------------------------------------------------------------
# WORKER THREAD (Unchanged from original)
# ---------------------------------------------------------------------------

def run_worker(worker_number, token, channel_id):
    """Run a single selfbot worker with prefix commands."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    label = f"[W#{worker_number:02d}]"
    retry_delay = RETRY_DELAY_INITIAL
    attempt = 0

    while True:
        attempt += 1
        if attempt > 1:
            log_retry(label, retry_delay, attempt)
            _time.sleep(retry_delay)
            retry_delay = min(retry_delay * RETRY_DELAY_FACTOR, RETRY_DELAY_MAX)

        try:
            bot = create_bot(worker_number)
            
            if attempt == 1:
                ws = WorkerState(worker_number)
                ws.bot = bot
                ws.auto_start_channel_id = channel_id
                ws.current_speed_mode = "efficient"  # Force efficient mode
                ws.huntbot_enabled = True             # Force huntbot on
                manager.register_worker(ws)
                register_commands(bot, ws)
            else:
                ws = manager.get_worker(worker_number)
                ws.bot = bot
                register_commands(bot, ws)

            @bot.event
            async def on_ready():
                ws.username = str(bot.user)
                log_worker_ready(worker_number, str(bot.user), ws.auto_start_channel_id)
                
                # Auto-start farming on ready
                if ws.auto_start_channel_id:
                    ch_id = ws.auto_start_channel_id
                    success, blocking = manager.try_claim_channel(ch_id, worker_number)
                    
                    if success:
                        target_channel = bot.get_channel(ch_id)
                        if target_channel:
                            pseudo_ctx = PseudoCtx(target_channel, bot)
                            asyncio.create_task(_run_farming_loop(pseudo_ctx, ws, bot))
                            log_info(f"[W#{worker_number:02d}] Auto-started farming in channel {ch_id}")
                    else:
                        log_warn(f"[W#{worker_number:02d}] Channel {ch_id} locked by another worker")

            @bot.event
            async def on_disconnect():
                log_disconnect(label)

            @bot.event
            async def on_resumed():
                log_resumed(label)

            @bot.event
            async def on_error(event, *args, **kwargs):
                import traceback
                log_event_error(label, event)
                traceback.print_exc()

            log_worker_start(worker_number)
            bot.run(token, log_handler=None)
            break

        except (KeyboardInterrupt, SystemExit):
            break
        except Exception as e:
            log_net_error(label, e)

    loop.close()


# ---------------------------------------------------------------------------
# MAIN CONTROLLER BOT (With Modal Panels)
# ---------------------------------------------------------------------------

import discord
from discord.ext import commands

class PanelView(discord.ui.View):
    """View with two buttons for modal interactions."""
    
    def __init__(self, bot_instance):
        super().__init__(persistent=False)
        self.bot = bot_instance
    
    @discord.ui.button(label="Add Tokens", style=discord.ButtonStyle.blurple, custom_id="btn_add_tokens")
    async def btn_add_tokens(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Open modal for token input."""
        modal = TokenModal()
        await interaction.response.send_modal(modal)
    
    @discord.ui.button(label="Add Channels", style=discord.ButtonStyle.blurple, custom_id="btn_add_channels")
    async def btn_add_channels(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Open modal for channel input."""
        modal = ChannelModal()
        await interaction.response.send_modal(modal)


class TokenModal(discord.ui.Modal, title="Add Worker Tokens"):
    """Modal for entering worker account tokens."""
    
    tokens_input = discord.ui.TextInput(
        label="Worker Tokens",
        placeholder="Single token or comma-separated: TOKEN1,TOKEN2,TOKEN3",
        style=discord.TextStyle.long,
        min_length=50,
        max_length=3000,
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Process token submission."""
        token_string = str(self.tokens_input).strip()
        tokens = _validate_tokens(token_string)
        
        if not tokens:
            await interaction.response.send_message(
                "❌ Invalid tokens. Please enter valid Discord user tokens.",
                ephemeral=True
            )
            return
        
        config_state.worker_tokens = tokens
        
        await interaction.response.send_message(
            f"✅ Loaded {len(tokens)} worker token(s).\n\n"
            f"Now add {len(tokens)} channel ID(s) with the **Add Channels** button.",
            ephemeral=True
        )
        
        # Check if both are configured
        if config_state.worker_tokens and config_state.channel_ids:
            if len(config_state.worker_tokens) == len(config_state.channel_ids):
                await _start_workers()


class ChannelModal(discord.ui.Modal, title="Add Channel IDs"):
    """Modal for entering channel IDs for workers."""
    
    channels_input = discord.ui.TextInput(
        label="Channel IDs",
        placeholder="Single ID or comma-separated: 1234567890,1234567891,1234567892",
        style=discord.TextStyle.long,
        min_length=10,
        max_length=2000,
        required=True
    )
    
    async def on_submit(self, interaction: discord.Interaction):
        """Process channel submission."""
        channel_string = str(self.channels_input).strip()
        channels = _validate_channels(channel_string)
        
        if not channels:
            await interaction.response.send_message(
                "❌ Invalid channel IDs. Please enter valid Discord channel IDs.",
                ephemeral=True
            )
            return
        
        config_state.channel_ids = channels
        
        await interaction.response.send_message(
            f"✅ Loaded {len(channels)} channel ID(s).\n\n"
            f"Now add {len(channels)} worker token(s) with the **Add Tokens** button.",
            ephemeral=True
        )
        
        # Check if both are configured
        if config_state.worker_tokens and config_state.channel_ids:
            if len(config_state.worker_tokens) == len(config_state.channel_ids):
                await _start_workers()


async def _start_workers():
    """Start all workers with configured tokens and channels."""
    if config_state.is_configured:
        return  # Already started
    
    if not config_state.worker_tokens or not config_state.channel_ids:
        return
    
    if len(config_state.worker_tokens) != len(config_state.channel_ids):
        log_warn(f"Token count ({len(config_state.worker_tokens)}) != Channel count ({len(config_state.channel_ids)})")
        return
    
    config_state.is_configured = True
    manager.set_has_channels_config(True)
    
    log_success(f"Configuration complete: {len(config_state.worker_tokens)} workers")
    
    # Start worker threads
    for worker_num, (token, channel_id) in enumerate(zip(config_state.worker_tokens, config_state.channel_ids), start=1):
        t = threading.Thread(
            target=run_worker,
            args=(worker_num, token, channel_id),
            daemon=True,
            name=f"Worker-{worker_num}"
        )
        t.start()
        log_info(f"Started worker thread #{worker_num} for channel {channel_id}")


class ControllerBot(commands.Cog):
    """Main controller with .panel command."""
    
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="panel")
    async def cmd_panel(self, ctx):
        """Display configuration panel with modals."""
        
        # Build current config status
        token_count = len(config_state.worker_tokens)
        channel_count = len(config_state.channel_ids)
        
        if config_state.is_configured:
            status = f"✅ **ACTIVE** — {token_count} worker(s) farming"
        elif token_count > 0 or channel_count > 0:
            status = f"⚠️ **PARTIAL** — {token_count} token(s), {channel_count} channel(s)"
        else:
            status = "🟡 **NOT CONFIGURED** — No tokens or channels set"
        
        embed = discord.Embed(
            title="🎮 GhoSty OwO — Configuration Panel",
            description=(
                "**⚠️ SECURITY WARNING** ⚠️\n"
                "Do not share your worker tokens with anyone!\n"
                "These grant full access to your Discord accounts.\n\n"
                "Token values will be submitted to this bot only.\n"
                "Only the bot operator can see configuration."
            ),
            color=discord.Color.blurple()
        )
        
        embed.add_field(
            name="Current Status",
            value=status,
            inline=False
        )
        
        embed.add_field(
            name="How to Configure",
            value=(
                "1. Click **Add Tokens** → Enter your worker account tokens\n"
                "   (Single token or comma-separated: `TOKEN1,TOKEN2,TOKEN3`)\n\n"
                "2. Click **Add Channels** → Enter channel IDs for each worker\n"
                "   (Must match token count: `CHANNEL1,CHANNEL2,CHANNEL3`)\n\n"
                "3. Farming starts automatically once configured\n"
                "   All workers set to **efficient** mode with **HuntBot ON**"
            ),
            inline=False
        )
        
        embed.add_field(
            name="⚙️ Default Settings",
            value="Speed Mode: **Efficient** 🐢\nHuntBot: **Enabled** 🎯",
            inline=False
        )
        
        embed.set_footer(text="Do not share this message or your tokens | GhoSty OwO V4")
        
        # Create view with buttons
        view = PanelView(self.bot)
        
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
            log_retry(label, retry_delay, attempt)
            _time.sleep(retry_delay)
            retry_delay = min(retry_delay * RETRY_DELAY_FACTOR, RETRY_DELAY_MAX)

        try:
            bot = loop.run_until_complete(setup_controller_bot())

            @bot.event
            async def on_disconnect():
                log_disconnect(label)

            @bot.event
            async def on_resumed():
                log_resumed(label)

            @bot.event
            async def on_error(event, *args, **kwargs):
                import traceback
                log_event_error(label, event)
                traceback.print_exc()

            log_info(f"{label} Starting with token: {token[:20]}...")
            bot.run(token, log_handler=None)
            break

        except Exception as e:
            log_net_error(label, e)

    loop.close()


# ---------------------------------------------------------------------------
# MAIN ENTRY POINT
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    threads = []

    # Start web dashboard if enabled
    if web_dashboard_enabled:
        try:
            from dashboard.app import start_server
            dash_t = threading.Thread(target=start_server, daemon=True, name="Dashboard")
            dash_t.start()
            threads.append(dash_t)
            log_success("Web dashboard started")
        except Exception as e:
            log_warn(f"Could not start dashboard: {e}")

    # Start main controller thread
    if main_token:
        t = threading.Thread(
            target=run_main_controller,
            args=(main_token,),
            daemon=True,
            name="MainController"
        )
        t.start()
        threads.append(t)
        log_success("Main controller thread started")

    # Wait for threads
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        log_shutdown()
        sys.exit(0)
