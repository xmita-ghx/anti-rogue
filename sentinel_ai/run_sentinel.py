"""
Sentinel AI — Unified Launcher
================================
Single entry point for all Sentinel AI operating modes.

Usage:
    python run_sentinel.py

Modes:
    1. Demo Mode          — automated hackathon demo via demo.py
    2. Autonomous Monitor — OCR-based dashboard monitoring via sentinel_monitor.py
    3. Voice Investigation — voice-controlled pipeline via main.py
"""

import os
import sys

# ── Path Safety ──────────────────────────────────────────────────────────────
# Ensure the working directory is sentinel_ai/ regardless of where
# the script is invoked from, so that local imports resolve correctly.

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(_SCRIPT_DIR)

if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)


# ── Banner ───────────────────────────────────────────────────────────────────

BANNER = """
╔═══════════════════════════════════════════════╗
║                                               ║
║      Sentinel AI Security Platform            ║
║      Autonomous AI SOC Agent                  ║
║                                               ║
╚═══════════════════════════════════════════════╝
"""

MENU = """
  Select system mode:

    1 — Demo Mode (Automated Hackathon Demo)
    2 — Autonomous Monitoring Mode
    3 — Voice Investigation Mode
    4 — Exit

"""


# ── Mode Runners ─────────────────────────────────────────────────────────────

def run_demo_mode():
    """Launch the automated demo pipeline from demo.py."""
    print()
    print("=" * 50)
    print("  Starting Sentinel Demo Mode...")
    print("=" * 50)
    print()

    try:
        from demo import run_demo
    except ImportError as e:
        print(f"  Error: demo.py could not be loaded.")
        print(f"  Details: {e}")
        return

    try:
        run_demo()
    except KeyboardInterrupt:
        print("\n  Demo interrupted by operator.")
    except Exception as e:
        print(f"\n  Sentinel encountered an error during execution.")
        print(f"  Details: {e}")


def run_monitor_mode():
    """Launch the autonomous monitoring loop from sentinel_monitor.py."""
    print()
    print("=" * 50)
    print("  Starting Sentinel Autonomous Monitoring...")
    print("=" * 50)
    print()

    try:
        from sentinel_monitor import start_monitor
    except ImportError as e:
        print(f"  Error: sentinel_monitor.py could not be loaded.")
        print(f"  Details: {e}")
        return

    try:
        start_monitor()
    except KeyboardInterrupt:
        print("\n  Monitoring interrupted by operator.")
    except Exception as e:
        print(f"\n  Sentinel encountered an error during execution.")
        print(f"  Details: {e}")


def run_voice_mode():
    """Launch the voice-controlled investigation pipeline from main.py."""
    print()
    print("=" * 50)
    print("  Starting Sentinel Voice Control Mode...")
    print("=" * 50)
    print()

    try:
        from main import main
    except ImportError as e:
        print(f"  Error: main.py could not be loaded.")
        print(f"  Details: {e}")
        return

    try:
        main()
    except KeyboardInterrupt:
        print("\n  Investigation interrupted by operator.")
    except Exception as e:
        print(f"\n  Sentinel encountered an error during execution.")
        print(f"  Details: {e}")


# ── Launcher Loop ────────────────────────────────────────────────────────────

def launcher():
    """Display the menu and dispatch to the selected mode in a loop."""

    print(BANNER)

    while True:
        print("=" * 50)
        print("  Sentinel AI Launcher")
        print("=" * 50)
        print(MENU)

        try:
            choice = input("  Enter choice: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n  Exiting Sentinel AI. Stay secure.\n")
            break

        if choice == "1":
            run_demo_mode()
        elif choice == "2":
            run_monitor_mode()
        elif choice == "3":
            run_voice_mode()
        elif choice == "4":
            print("\n  Exiting Sentinel AI. Stay secure.\n")
            break
        else:
            print(f"\n  Invalid choice: '{choice}'. Please enter 1–4.\n")
            continue

        # After any mode completes, pause before returning to menu
        print()
        input("  Press Enter to return to launcher...")
        print()


# ── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    launcher()
