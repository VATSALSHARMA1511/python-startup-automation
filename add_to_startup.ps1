# add_to_startup.ps1
# ------------------
# Adds a shortcut to startup_launcher.py in your Windows Startup folder.
# Run this script ONCE after testing with test_launcher.py.
#
# How to run:
#   1. Open PowerShell (not as admin — regular user is fine)
#   2. Navigate to this folder:  cd "C:\path\to\startup_automation"
#   3. Run:  .\add_to_startup.ps1
#
# To REMOVE from startup, delete the shortcut:
#   Run:  .\add_to_startup.ps1 -Remove
#
# What this does:
#   Creates a .lnk shortcut in shell:startup that points to pythonw.exe
#   running startup_launcher.py. Uses pythonw.exe (not python.exe) so
#   no black console window flashes on screen at startup.

param(
    [switch]$Remove  # Pass -Remove to delete the shortcut instead of creating it
)

# ── Paths ────────────────────────────────────────────────────────────────────

# The Windows Startup folder path
$StartupFolder = [System.Environment]::GetFolderPath("Startup")
$ShortcutPath  = Join-Path $StartupFolder "StartupLauncher.lnk"

# The script file (in the same folder as this .ps1 file)
$ScriptFile    = Join-Path $PSScriptRoot "startup_launcher.py"

# pythonw.exe — same as python.exe but runs WITHOUT a console window
# We find it from the running Python's path
$PythonW       = (Get-Command python).Source -replace "python\.exe$", "pythonw.exe"


# ── Remove mode ──────────────────────────────────────────────────────────────

if ($Remove) {
    if (Test-Path $ShortcutPath) {
        Remove-Item $ShortcutPath -Force
        Write-Host "✓ Shortcut removed from Startup folder." -ForegroundColor Green
        Write-Host "  Path was: $ShortcutPath"
    } else {
        Write-Host "  No shortcut found at: $ShortcutPath" -ForegroundColor Yellow
        Write-Host "  Nothing to remove."
    }
    exit 0
}


# ── Add mode ─────────────────────────────────────────────────────────────────

# Check the script file exists
if (-not (Test-Path $ScriptFile)) {
    Write-Host "✗ startup_launcher.py not found at: $ScriptFile" -ForegroundColor Red
    Write-Host "  Make sure this .ps1 file is in the same folder as startup_launcher.py"
    exit 1
}

# Check pythonw.exe exists
if (-not (Test-Path $PythonW)) {
    Write-Host "✗ pythonw.exe not found at: $PythonW" -ForegroundColor Red
    Write-Host "  Make sure Python is properly installed."
    exit 1
}

# Create the shortcut using Windows Shell COM object
# (This is the standard Windows-native way to create .lnk files)
$WshShell  = New-Object -ComObject WScript.Shell
$Shortcut  = $WshShell.CreateShortcut($ShortcutPath)

$Shortcut.TargetPath       = $PythonW                         # Run with pythonw.exe (no console window)
$Shortcut.Arguments        = "`"$ScriptFile`""               # The script to run (quoted for spaces in path)
$Shortcut.WorkingDirectory = $PSScriptRoot                    # Set working dir to script folder
$Shortcut.WindowStyle      = 7                                # 7 = minimized (so nothing flashes on screen)
$Shortcut.Description      = "Startup automation launcher"

$Shortcut.Save()

Write-Host ""
Write-Host "✓ Shortcut added to Windows Startup folder." -ForegroundColor Green
Write-Host ""
Write-Host "  Shortcut location : $ShortcutPath"
Write-Host "  Runs              : $PythonW"
Write-Host "  Script            : $ScriptFile"
Write-Host ""
Write-Host "  To verify: press Win+R, type shell:startup, press Enter."
Write-Host "  You should see 'StartupLauncher.lnk' in that folder."
Write-Host ""
Write-Host "  To remove later, run:  .\add_to_startup.ps1 -Remove"
