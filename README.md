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

