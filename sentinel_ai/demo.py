"""
Sentinel AI — Unified System Launcher
-------------------------------------
The single public entry point for the Sentinel AI system.
Orchestrates the startup of the SOC dashboard, the control panel,
and initializes Sentinel AI hooks cleanly.
"""

import time
import webbrowser

# ── Configuration ────────────────────────────────────────────────────────────

DASHBOARD_URL = "http://localhost:3000"


# ── Internal Demo Logic (Preserved for compatibility) ────────────────────────

def run_demo():
    print("=" * 60)
    print("         SENTINEL AI — AUTOMATED DEMO MODE")
    print("=" * 60)
    print()
    print("Demo Mode Starting...")
    print()

    print("Step 1: Triggering rogue AI agent...")
    from rogue import trigger_rogue_agent
    success = trigger_rogue_agent()
    
    if not success:
        print("ERROR: Failed to automatically trigger rogue agent.")
        print(f"Please open {DASHBOARD_URL} in your browser first.")
        return

    print("\nStep 5: Waiting for dashboard to update...")
    time.sleep(3)

    print("\n" + "=" * 60)
    print("  Starting Sentinel AI investigation...")
    print("=" * 60)
    print()

    from main import main
    main(simulated_command="scan")


# ── System Orchestration (Public Entry Point) ────────────────────────────────

def initialize_sentinel_hooks():
    """Import and test Sentinel hooks to ensure system subsystem readiness. Does not start the loops."""
    print("  [init] Initializing Sentinel system hooks...")
    try:
        import main
        import sentinel_monitor
        import desktop_controller
        print("  [init] Core modules loaded successfully.")
    except Exception as e:
        print(f"  [init] ERROR: Failed to load core modules: {e}")

def start_dashboard():
    """Ensure the dashboard is open in the default browser."""
    print(f"  [init] Opening {DASHBOARD_URL} in browser...")
    try:
        webbrowser.open(DASHBOARD_URL)
        time.sleep(2)  # Allow time for the browser to launch
    except Exception as e:
        print(f"  [init] ERROR: Failed to open dashboard: {e}")

def start_control_panel():
    """Start the Tkinter control panel."""
    print("  [init] Launching Sentinel Control Panel...")
    try:
        from sentinel_control_panel import SentinelControlPanel
        app = SentinelControlPanel()
        app.run()
    except Exception as e:
        print(f"  [init] ERROR: Failed to launch Control Panel: {e}")

def system_boot():
    """Main orchestrator for the entire Sentinel AI system."""
    print("=" * 60)
    print("         SENTINEL AI — SYSTEM UNIFIED LAUNCHER")
    print("=" * 60)
    print()
    print("Boot sequence starting...")
    print()
    
    try:
        # Step 1: Initialize System Hooks (ensure modules are reachable)
        initialize_sentinel_hooks()
        print()
        
        # Step 2: Ensure Dashboard is open
        start_dashboard()
        print()
        
        # Step 3: Start the Control Panel (Main Loop)
        start_control_panel()
        
    except KeyboardInterrupt:
        print("\n[SYSTEM] Shutdown requested by user.")
    except Exception as e:
        print(f"\n[SYSTEM] Terminal error during boot: {e}")
    finally:
        print("\n[SYSTEM] Sentinel AI shutdown complete.")

if __name__ == "__main__":
    system_boot()
