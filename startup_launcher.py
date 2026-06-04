"""
startup_launcher.py
-------------------
Opens Spotify (with a track), VSCode, and Chrome (Gmail + ChatGPT)
when Windows starts up. Uses only Python standard library — no installs needed.

How it works:
  1. Runs once at login via the Windows Startup folder shortcut
  2. Opens apps one by one with short delays between them
  3. Writes a log file so you can debug if anything goes wrong
  4. Exits cleanly — no background process remains after launch
"""

# ── Standard library imports only ──────────────────────────────────────────
import subprocess   # Lets Python run external programs (like opening apps)
import time         # Lets Python pause between launching apps
import logging      # Writes timestamped messages to a log file for debugging
import sys          # Gives us the Python interpreter path and exit control
from pathlib import Path  # Safe, cross-platform way to work with file paths


# ── Configuration — edit these if your setup changes ───────────────────────

# The Spotify track URI you want to autoplay
SPOTIFY_URI = "spotify:track:2JuasWPUodaUxf5nwNpciQ"

# Chrome URLs to open (each becomes its own tab)
CHROME_URLS = [
    "https://mail.google.com",
    "https://chatgpt.com",
]

# Delays between launching each app (in seconds)
# Why delays? So your laptop isn't trying to load 4 apps at the exact same time.
# Adjust these if apps feel too slow/fast on your machine.
DELAY_AFTER_SPOTIFY = 5   # seconds to wait after Spotify before opening VSCode
DELAY_AFTER_VSCODE  = 7   # seconds to wait after VSCode before opening Chrome

# Where to save the log file (same folder as this script)
LOG_FILE = Path(__file__).parent / "logs" / "startup_log.txt"


# ── Logging setup ───────────────────────────────────────────────────────────
# This creates a log file that records every step with timestamps.
# If something breaks, open the log file to see exactly what happened and when.

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)  # Create the logs/ folder if it doesn't exist

logging.basicConfig(
    level=logging.INFO,                # Record INFO and above (INFO, WARNING, ERROR)
    format="%(asctime)s  %(levelname)-8s  %(message)s",  # e.g. "2024-01-15 08:32:01  INFO     Launching Spotify"
    handlers=[
        logging.FileHandler(LOG_FILE, encoding="utf-8"),  # Write to file
        logging.StreamHandler(sys.stdout),                 # Also print to console (useful when testing)
    ],
)

log = logging.getLogger(__name__)  # Get a logger named after this file


# ── Helper function ─────────────────────────────────────────────────────────

def launch(description: str, command: list[str]) -> bool:
    """
    Runs a command to open an application.

    Args:
        description: Human-readable name, used only for logging (e.g. "Spotify")
        command:     The command as a list of strings (e.g. ["start", "", "spotify:..."])

    Returns:
        True if the command launched without error, False if it failed.

    Why subprocess.run() instead of os.system()?
        subprocess.run() is the modern, safe way. It gives us the return code,
        doesn't open an extra terminal window, and handles errors cleanly.

    Why shell=True?
        Because we're using Windows shell commands like "start". The "start"
        command is built into cmd.exe (not a standalone .exe file), so we
        need the shell to interpret it.
    """
    log.info(f"Launching {description} ...")

    try:
        result = subprocess.run(
            command,
            shell=True,          # Required for "start" and other shell built-ins
            check=False,         # Don't raise an exception — we handle errors ourselves
            capture_output=True, # Capture any error messages the command prints
            text=True,           # Return output as string (not raw bytes)
        )

        if result.returncode != 0:
            # returncode 0 = success, anything else = something went wrong
            log.warning(f"{description} returned exit code {result.returncode}. stderr: {result.stderr.strip()}")
            return False

        log.info(f"{description} launched successfully.")
        return True

    except Exception as e:
        # Catch any unexpected error (e.g. Python itself crashed trying to run the command)
        log.error(f"Failed to launch {description}: {e}")
        return False


# ── Main sequence ───────────────────────────────────────────────────────────

def main():
    """
    The main launch sequence. Apps open one by one with delays between them.
    """
    log.info("=" * 60)
    log.info("Startup launcher started.")
    log.info("=" * 60)

    # ── Step 1: Open Spotify and play the track ─────────────────────────────
    # How this works:
    #   "start" is a Windows shell command that opens a file/URI using its
    #   default handler — just like double-clicking it in Explorer.
    #   The second "" is required by "start" as a window title argument
    #   (without it, the URI would be treated as the window title).
    #   Windows knows Spotify handles "spotify:" URIs, so it opens Spotify
    #   and immediately begins playing the track.

    launch("Spotify", ["start", "", SPOTIFY_URI])

    # Wait before opening the next app. This prevents all apps from
    # competing for CPU/disk at the exact same moment on startup.
    log.info(f"Waiting {DELAY_AFTER_SPOTIFY}s before launching VSCode ...")
    time.sleep(DELAY_AFTER_SPOTIFY)


    # ── Step 2: Open VSCode ─────────────────────────────────────────────────
    # "code" is the VSCode command-line command — the VSCode installer adds
    # it to your PATH automatically.
    # We open VSCode without specifying a folder, so it restores your last session.
    # If you want to always open a specific folder, replace "code" with:
    #   ["code", r"C:\Users\YourName\Projects\my-project"]

    launch("VSCode", ["code"])

    log.info(f"Waiting {DELAY_AFTER_VSCODE}s before launching Chrome ...")
    time.sleep(DELAY_AFTER_VSCODE)


    # ── Step 3: Open Chrome with Gmail and ChatGPT ──────────────────────────
    # Chrome supports opening multiple URLs at once from the command line.
    # The first URL opens in the current tab; extras open as additional tabs.
    # "start chrome" uses Windows to find Chrome — no need to hard-code the path.

    launch("Chrome", ["start", "chrome"] + CHROME_URLS)


    # ── Done ────────────────────────────────────────────────────────────────
    log.info("All apps launched. Startup launcher finished.")
    log.info("=" * 60)

    # The script exits here. No background process remains.


# ── Entry point ─────────────────────────────────────────────────────────────
# This block runs only when you execute the file directly (python startup_launcher.py).
# It does NOT run if another script imports this file as a module.

if __name__ == "__main__":
    main()
