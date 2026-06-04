"""
test_launcher.py
----------------
Run this BEFORE adding anything to Windows Startup.
It checks that each app command works correctly on your machine.

How to run:
    python test_launcher.py

What it does:
    - Tests each launch command individually
    - Confirms Spotify URI works
    - Confirms "code" command is on your PATH
    - Confirms Chrome opens correctly
    - Reports any failures BEFORE they affect your startup routine

SAFE TO RUN AT ANY TIME. Does not modify Windows startup or any system settings.
"""

import subprocess
import sys
import time
from pathlib import Path


def check_python_version():
    """Confirm we're on Python 3.9+ (required for list[str] type hints)."""
    major, minor = sys.version_info[:2]
    if major < 3 or minor < 9:
        print(f"  ✗  Python {major}.{minor} is too old. Need 3.9+.")
        return False
    print(f"  ✓  Python {major}.{minor}.{sys.version_info[2]} — OK")
    return True


def check_command_on_path(command_name: str) -> bool:
    """Check if a command is available on the system PATH."""
    # 'where' is Windows' equivalent of 'which' on Linux/Mac
    result = subprocess.run(
        ["where", command_name],
        capture_output=True,
        text=True,
        shell=False,
    )
    if result.returncode == 0:
        path = result.stdout.strip().splitlines()[0]
        print(f"  ✓  '{command_name}' found at: {path}")
        return True
    else:
        print(f"  ✗  '{command_name}' NOT found on PATH. Check your installation.")
        return False


def test_spotify_uri():
    """Open Spotify with the configured track URI."""
    from startup_launcher import SPOTIFY_URI
    print(f"\n  → Sending URI to Spotify: {SPOTIFY_URI}")
    result = subprocess.run(["start", "", SPOTIFY_URI], shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✓  Spotify URI command sent successfully.")
        print("     Check: did Spotify open and start playing?")
    else:
        print(f"  ✗  Spotify command failed (exit code {result.returncode})")
        print(f"     Error: {result.stderr.strip()}")


def test_vscode():
    """Open VSCode."""
    print("\n  → Opening VSCode ...")
    result = subprocess.run(["code"], shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✓  VSCode launched.")
    else:
        print(f"  ✗  VSCode failed (exit code {result.returncode})")
        print("     Make sure VSCode is installed and 'code' is on your PATH.")
        print("     In VSCode: press F1 → 'Shell Command: Install code command in PATH'")


def test_chrome():
    """Open Chrome with Gmail and ChatGPT."""
    from startup_launcher import CHROME_URLS
    print(f"\n  → Opening Chrome with {len(CHROME_URLS)} tabs ...")
    result = subprocess.run(["start", "chrome"] + CHROME_URLS, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print("  ✓  Chrome launched.")
        print(f"     Check: did you get {len(CHROME_URLS)} tabs?")
    else:
        print(f"  ✗  Chrome failed (exit code {result.returncode})")
        print("     Make sure Chrome is installed. Alternatively, replace 'chrome' with the full path.")


def check_log_folder():
    """Make sure the logs directory will be writable."""
    log_dir = Path(__file__).parent / "logs"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
        test_file = log_dir / ".writetest"
        test_file.write_text("ok")
        test_file.unlink()
        print(f"  ✓  Log folder writable: {log_dir}")
        return True
    except Exception as e:
        print(f"  ✗  Cannot write to log folder: {e}")
        return False


# ── Run all tests ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 52)
    print("  Startup Launcher — Pre-flight checks")
    print("=" * 52)

    print("\n[1] Python version")
    check_python_version()

    print("\n[2] Required commands on PATH")
    check_command_on_path("code")    # VSCode

    print("\n[3] Log folder writable")
    check_log_folder()

    print("\n[4] Live app tests")
    print("     Each test will actually open the app.")
    input("     Press ENTER to begin (or Ctrl+C to cancel) ...")

    test_spotify_uri()
    time.sleep(4)

    test_vscode()
    time.sleep(6)

    test_chrome()

    print("\n" + "=" * 52)
    print("  All tests complete. Check the results above.")
    print("  If all show ✓, you're ready to add to Startup.")
    print("=" * 52)
