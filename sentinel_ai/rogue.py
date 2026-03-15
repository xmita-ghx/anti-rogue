"""
Rogue Agent Trigger Helper
--------------------------
Finds the SOC dashboard in an open browser, injects a command
via the developer console to simulate a rogue agent attack,
and safely closes the console.
"""

import time
import pyautogui
import pygetwindow as gw

DASHBOARD_KEYWORDS = [
    "Security Operations", "SOC Dashboard", "Sentinel SOC",
    "Sentinel AI Security", "localhost",
]
BROWSER_KEYWORDS = ["brave", "chrome", "edge", "firefox", "opera"]
EXCLUDED_TITLES = ["Sentinel AI Digital Console", "Antigravity"]
ROGUE_TRIGGER_CMD = "triggerRogueAgent()"

def get_dashboard_window():
    """
    Find the SOC dashboard browser window.
    Strategy:
      1. First, look for a window whose title contains a dashboard-specific keyword.
      2. If not found (tab may be in background), fall back to any browser window
         that is NOT the Sentinel control panel or the IDE.
    """
    all_windows = gw.getAllWindows()

    # Pass 1: exact dashboard keyword match
    for window in all_windows:
        title = window.title
        if not title:
            continue
        if any(ex.lower() in title.lower() for ex in EXCLUDED_TITLES):
            continue
        if any(kw.lower() in title.lower() for kw in DASHBOARD_KEYWORDS):
            return window

    # Pass 2: fallback — any browser window (dashboard tab may be in background)
    for window in all_windows:
        title = window.title
        if not title:
            continue
        if any(ex.lower() in title.lower() for ex in EXCLUDED_TITLES):
            continue
        if any(br in title.lower() for br in BROWSER_KEYWORDS):
            return window

    return None

def trigger_rogue_agent() -> bool:
    """
    Locates the SOC dashboard, opens the browser console,
    injects the rogue agent trigger, and closes the console.
    
    Returns:
        True if the trigger was executed successfully, False otherwise.
    """
    print("[Rogue Helper] Locating SOC dashboard...")
    window = get_dashboard_window()

    if window is None:
        print("[Rogue Helper] ERROR: SOC dashboard window not found.")
        return False

    print("[Rogue Helper] Window found. Attempting to focus...")
    try:
        window.activate()
    except Exception:
        try:
            window.minimize()
            time.sleep(0.3)
            window.restore()
        except Exception as e:
            print(f"[Rogue Helper] WARNING: Could not reliably focus window: {e}")
            pass
    
    time.sleep(0.5)

    try:
        print("[Rogue Helper] Opening browser developer console...")
        pyautogui.hotkey("ctrl", "shift", "j")
        time.sleep(1.5)

        print(f"[Rogue Helper] Injecting trigger: {ROGUE_TRIGGER_CMD}")
        import subprocess
        subprocess.run(["clip"], input=ROGUE_TRIGGER_CMD.encode(), check=True)
        pyautogui.hotkey("ctrl", "v")
        time.sleep(0.5)
        pyautogui.press("escape")   # dismiss any autocomplete popup
        time.sleep(0.2)
        pyautogui.press("enter")
        time.sleep(1.0)

        print("[Rogue Helper] Closing developer console...")
        pyautogui.hotkey("ctrl", "shift", "j")
        time.sleep(0.5)

        print("[Rogue Helper] SUCCESS: Rogue agent triggered.")
        return True
    except Exception as e:
        print(f"[Rogue Helper] ERROR during rogue execution: {e}")
        return False

if __name__ == "__main__":
    trigger_rogue_agent()
