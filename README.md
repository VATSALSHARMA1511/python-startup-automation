# Startup Automation — Beginner Guide
A lightweight Windows startup launcher using only Python's standard library.
No registry edits. No background services. No heavy dependencies.

---

## Folder structure

```
startup_automation/
│
├── startup_launcher.py     ← The main script (edit config at the top)
├── test_launcher.py        ← Run this FIRST to verify everything works
├── add_to_startup.ps1      ← Adds/removes the Windows Startup shortcut
├── README.md               ← This file
│
└── logs/
    └── startup_log.txt     ← Auto-created. Check here if anything breaks.
```

---

## Step-by-step setup

### Step 1 — Test manually first
Open a terminal in this folder and run:
```
python test_launcher.py
```
Follow the prompts. Each app should open. Fix any failures before continuing.

### Step 2 — Add to Windows Startup
Open PowerShell (not as administrator) in this folder:
```
.\add_to_startup.ps1
```
This creates a shortcut in your Windows Startup folder. That's all.

### Step 3 — Verify
Press `Win + R`, type `shell:startup`, press Enter.
You should see `StartupLauncher.lnk` in that folder.

### Step 4 — Test at startup
Restart your laptop. After logging in, wait about 15 seconds.
All three apps should open automatically.

---

## How to remove from startup
```powershell
.\add_to_startup.ps1 -Remove
```
Or manually: press `Win + R` → `shell:startup` → delete `StartupLauncher.lnk`.

---

## Adjusting the delays
Open `startup_launcher.py` and change these two lines near the top:
```python
DELAY_AFTER_SPOTIFY = 5   # increase this if Spotify feels rushed
DELAY_AFTER_VSCODE  = 7   # increase this if VSCode feels slow to appear
```

---

## Checking the log file
If something doesn't open, check `logs/startup_log.txt`.
It records every step with timestamps so you can see exactly where it stopped.

---

## Failure cases and fixes

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| Spotify doesn't play | URI is wrong | Test URI manually: Win+R → paste `spotify:track:2JuasWPUodaUxf5nwNpciQ` |
| VSCode doesn't open | `code` not on PATH | In VSCode: F1 → "Shell Command: Install code command in PATH" |
| Chrome opens wrong tabs | URL typo | Check CHROME_URLS in startup_launcher.py |
| Nothing opens at startup | Shortcut broken | Re-run add_to_startup.ps1 |
| Console window flashes | Wrong Python used | Script uses pythonw.exe — check the shortcut's Target field |
| Script runs but apps don't appear | Delays too short | Increase DELAY_AFTER_SPOTIFY and DELAY_AFTER_VSCODE |

---

## Converting to an .exe (optional)

If you want a standalone `.exe` that doesn't need Python installed:

```
pip install pyinstaller
pyinstaller --onefile --noconsole startup_launcher.py
```

This creates `dist/startup_launcher.exe`. Use that path in `add_to_startup.ps1`
by changing `$PythonW` and `$ScriptFile` to just point at the .exe directly.

Only do this if you ever need to run it on a machine without Python.

---

## Suggested next automation projects (in order of difficulty)

1. **Daily folder cleanup** — move downloaded files into sorted subfolders by type
   Uses: `os`, `shutil`, `pathlib` — all standard library
   
2. **Auto-backup script** — copy specific folders to a backup location with a timestamp
   Uses: `shutil.copytree()`, `datetime` — all standard library
   
3. **Screenshot + clipboard tool** — capture and save screenshots on a hotkey
   Uses: `pyautogui` (which you already have), `Pillow`
   
4. **System health logger** — log CPU, RAM, disk usage every N minutes
   Uses: `psutil` (one small install), `csv`, `schedule`

5. **Auto-type text snippets** — expand short abbreviations into full text
   Uses: `pynput` (one install) — a natural next step for pyautogui users

---

## Best practices for future automation projects

- **Always test manually before adding to startup.** The 2 minutes saved on setup costs 20 minutes debugging why your laptop won't start right.
- **Log everything.** A `logging.basicConfig(...)` call at the top of every script costs nothing and saves hours.
- **Use `pathlib.Path` for all file paths.** Never hardcode `C:\\Users\\YourName\\...` — it breaks when you change username or PC.
- **Use `subprocess.run()` over `os.system()`.** It's safer, gives you error codes, and doesn't rely on a shell being available.
- **One script = one job.** Don't make a mega-script that does 10 things. Keep each automation focused.
- **Keep config at the top.** Put all the values you might change (delays, paths, URLs) as constants at the very top of the file — not buried in the code.
- **Version control from day one.** Even personal scripts benefit from `git init`. You'll thank yourself when something breaks.
