"""
Sentinel Monitor
-----------------
Continuously monitors the SOC dashboard by capturing screenshots
and performing OCR to detect when the Threat Level becomes CRITICAL.

When CRITICAL is detected:
  - Sends a desktop notification via plyer
  - Triggers startSentinelAlert() on the dashboard via browser console
  - Opens a 5-second operator response window

Usage:
    from sentinel_monitor import start_monitor
    start_monitor()
"""

import os
import time
import threading

import pyautogui
from PIL import Image

import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

try:
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False
from plyer import notification

# Import the investigation pipeline from main (lazy to avoid circular imports)
_investigation_pipeline = None

def _get_pipeline():
    """Lazily import run_investigation_pipeline to avoid circular imports."""
    global _investigation_pipeline
    if _investigation_pipeline is None:
        from main import run_investigation_pipeline
        _investigation_pipeline = run_investigation_pipeline
    return _investigation_pipeline



# ── Configuration ────────────────────────────────────────────────────────────

# Screenshot save path (relative to this script's directory)
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SCREENSHOT_PATH = os.path.join(_SCRIPT_DIR, "monitor_screen.png")

# Monitoring interval in seconds
MONITOR_INTERVAL = 5

# Keyword to detect
CRITICAL_KEYWORD = "CRITICAL"

# Operator response window duration
RESPONSE_WINDOW = 5


# ── Alert Helpers ────────────────────────────────────────────────────────────

def _send_desktop_notification():
    """
    Send a Windows desktop notification via plyer.
    """
    try:
        notification.notify(
            title="Sentinel AI Alert",
            message=(
                "Critical threat detected on SOC dashboard\n"
                "Awaiting operator response"
            ),
            app_name="Sentinel AI",
            timeout=10,
        )
        print("  Desktop notification sent")
    except Exception as e:
        print(f"  ⚠️  Desktop notification failed: {e}")


def _trigger_dashboard_alert():
    """
    Focus the browser window, open the developer console,
    and execute startSentinelAlert() on the SOC dashboard.
    """
    try:
        print("  Opening browser console...")
        time.sleep(0.5)

        # Open Chrome DevTools console (Ctrl+Shift+J)
        pyautogui.hotkey("ctrl", "shift", "j")
        time.sleep(1.5)

        # Type the function call
        pyautogui.typewrite("startSentinelAlert()", interval=0.03)
        time.sleep(0.3)

        # Execute it
        pyautogui.press("enter")
        time.sleep(0.5)

        # Close the console (Ctrl+Shift+J again)
        pyautogui.hotkey("ctrl", "shift", "j")
        time.sleep(0.3)

        print("  Dashboard alert triggered")
    except Exception as e:
        print(f"  ⚠️  Dashboard alert trigger failed: {e}")


# ── Operator Response Window ─────────────────────────────────────────────────

def _operator_response_window():
    """
    Run a 5-second countdown while listening for operator input.

    Returns:
        A string: "cancel", "investigate", "proceed", or "timeout".
    """
    print()
    print("=" * 40)
    print("   SENTINEL RESPONSE WINDOW")
    print("=" * 40)
    print()
    print("  Operator response window active")
    print()
    print("  Commands: 'cancel'  — abort autonomous action")
    print("            'investigate' — trigger investigation")
    print("            'proceed' — skip countdown")
    print()

    # Shared state between threads
    result = {"command": None}

    def _input_listener():
        """Background thread: waits for operator keyboard input."""
        try:
            user_input = input("  >> ").strip().lower()
            if user_input:
                result["command"] = user_input
        except (EOFError, KeyboardInterrupt):
            pass
        except Exception:
            pass

    # Start the input listener in a daemon thread
    listener = threading.Thread(target=_input_listener, daemon=True)
    listener.start()

    # Countdown loop
    for remaining in range(RESPONSE_WINDOW, 0, -1):
        # Check if operator already responded
        if result["command"] is not None:
            break

        print(f"  Auto containment in: {remaining}")
        time.sleep(1)

    # Final check
    if result["command"] is not None:
        return result["command"]

    print()
    return "timeout"


def _run_autonomous_containment():
    """
    Run the full Sentinel AI investigation and containment pipeline.
    Wraps run_investigation_pipeline() with logging and error handling.
    """
    print()
    print("=" * 40)
    print("   AUTONOMOUS CONTAINMENT")
    print("=" * 40)
    print()
    print("  Autonomous investigation started")
    print()

    try:
        pipeline = _get_pipeline()
        analysis, agent_id = pipeline()

        if analysis is None:
            print("  ⚠️  Investigation pipeline could not start.")
            print("  Ensure the SOC dashboard is open in the browser.")
            return

        if analysis.get("threat_detected"):
            print()
            print("  ✅ Autonomous containment completed")
            print(f"  Agent {agent_id} has been quarantined.")
        else:
            print()
            print("  ✅ Investigation complete — no threats detected.")

    except Exception as e:
        print(f"  ⚠️  Autonomous investigation failed: {e}")
        print("  Manual intervention may be required.")

    print()


# ── Public API ───────────────────────────────────────────────────────────────

def start_monitor():
    """
    Start a continuous monitoring loop that captures the screen every
    5 seconds, runs OCR, and checks for the word 'CRITICAL'.

    Stops automatically when CRITICAL is detected.
    """
    if not OCR_AVAILABLE:
        print("  ⚠️  pytesseract not found. Continuous monitoring depends on OCR and cannot start.")
        return

    print()
    print("=" * 50)
    print("       SENTINEL CONTINUOUS MONITOR")
    print("=" * 50)
    print()
    print(f"  Interval   : {MONITOR_INTERVAL}s")
    print(f"  Watching for: '{CRITICAL_KEYWORD}' keyword")
    print(f"  Screenshot : {SCREENSHOT_PATH}")
    print()
    print("-" * 50)
    print()

    cycle = 0

    while True:
        cycle += 1
        timestamp = time.strftime("%H:%M:%S")

        print(f"[{timestamp}] Cycle {cycle} — Monitoring dashboard...")

        # ── Step 1: Capture screenshot ───────────────────────────────
        try:
            screenshot = pyautogui.screenshot()
            screenshot.save(SCREENSHOT_PATH)
            print(f"[{timestamp}] Screenshot captured")
        except Exception as e:
            print(f"[{timestamp}] ⚠️  Screenshot capture failed: {e}")
            print(f"[{timestamp}] Retrying in {MONITOR_INTERVAL}s...")
            time.sleep(MONITOR_INTERVAL)
            continue

        # ── Step 2: OCR scan ─────────────────────────────────────────
        print(f"[{timestamp}] Scanning for CRITICAL threat level...")

        try:
            image = Image.open(SCREENSHOT_PATH)
            ocr_text = pytesseract.image_to_string(image)
        except Exception as e:
            print(f"[{timestamp}] ⚠️  OCR failed: {e}")
            print(f"[{timestamp}] Retrying in {MONITOR_INTERVAL}s...")
            time.sleep(MONITOR_INTERVAL)
            continue

        # ── Step 3: Check for CRITICAL ───────────────────────────────
        if CRITICAL_KEYWORD in ocr_text.upper():
            print()
            print("=" * 40)
            print("   SENTINEL MONITOR ALERT")
            print("=" * 40)
            print()
            print("  Critical threat level detected on dashboard")
            print()
            print("=" * 40)
            print()

            # ── Alert notifications ──────────────────────────────────
            print("Triggering Sentinel alert...")
            _send_desktop_notification()
            _trigger_dashboard_alert()
            print()

            # ── Operator response window ─────────────────────────────
            operator_cmd = _operator_response_window()

            if operator_cmd == "cancel":
                print()
                print("  Operator cancelled autonomous action.")
                print("  Returning to manual mode.")
                print()
            elif operator_cmd == "investigate":
                print()
                print("  Operator requested investigation.")
                print("  Sentinel AI initiating investigation...")
                _run_autonomous_containment()
            elif operator_cmd == "proceed":
                print()
                print("  Operator confirmed. Skipping countdown.")
                print("  Sentinel AI initiating investigation...")
                _run_autonomous_containment()
            else:
                # timeout
                print("  No operator response detected")
                print("  Switching to autonomous mode")
                print("  Sentinel AI initiating investigation...")
                _run_autonomous_containment()

            break
        else:
            print(f"[{timestamp}] Status: No critical threat detected.")
            print(f"[{timestamp}] Next scan in {MONITOR_INTERVAL}s...")
            print()

        # ── Wait before next cycle ───────────────────────────────────
        time.sleep(MONITOR_INTERVAL)

    print("Monitor stopped.")


# ── Direct execution ─────────────────────────────────────────────────────────

if __name__ == "__main__":
    start_monitor()

