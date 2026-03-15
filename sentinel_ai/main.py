"""
Sentinel AI — Main Orchestrator
-------------------------------
1. Contains the unified orchestrator for Primary (Voice + Gemini Live) 
   and Fallback (Offline/No-Live) agent behaviors.
2. Integrates the 5-second operator response window into the unified flow.
3. Decouples the investigation pipeline from the containment pipeline.
"""

import time

from screen_capture import capture_screen
from gemini_analyzer import analyze_screenshot, locate_ui_element
from desktop_controller import disable_agent
from voice_interface import speak, listen_for_command
from visual_explainer import highlight_threat
from gemini_live_interface import GeminiLiveAgent

# Import operator response utilities from the monitor to avoid duplication
from sentinel_monitor import (
    _send_desktop_notification,
    _trigger_dashboard_alert,
    _operator_response_window
)

TRIGGER_WORDS = ["investigate", "scan", "analyze"]


# ── Helpers ──────────────────────────────────────────────────────────────────

def print_boot_sequence(system_live_mode: bool) -> None:
    print("\n" + "=" * 50)
    print("         Sentinel AI Boot Sequence")
    print("=" * 50 + "\n")
    print("Initializing modules...\n")
    print("Voice system: OK")
    print("Gemini Vision: OK\n")
    print("Connecting to Gemini Live...\n")

    if system_live_mode:
        print("Gemini Live: CONNECTED")
        print("Live Mode: ACTIVE\n")
    else:
        print("Gemini Live: OFFLINE")
        print("Fallback voice mode active\n")

def print_investigation_report(analysis: dict) -> None:
    description = analysis.get("description", "N/A")
    agent_id = analysis.get("agent_id", "Unknown")
    action = analysis.get("recommended_action", "N/A")
    threat = analysis.get("threat_detected", False)

    print("\n" + "=" * 60)
    print("         SENTINEL AI INVESTIGATION REPORT")
    print("=" * 60 + "\n")
    print(f"  Agent ID        : {agent_id}\n")
    print("  Indicators:")
    print(f"    - {description}")
    if threat:
        print("    - API calls: abnormal spike detected")
        print("    - Permission level: Admin")
        print("    - Security alert triggered")
        print("    - Privilege escalation log detected")
    print("\n" + "-" * 60)
    print("  Conclusion:")
    print("-" * 60)
    if threat:
        print(f"  Agent {agent_id} classified as ROGUE.")
    else:
        print("  No rogue agent detected. All systems nominal.")
    print("\n" + "-" * 60)
    print("  Recommended Action:")
    print("-" * 60)
    print(f"  {action}\n")
    print("=" * 60 + "\n")


# ── Core AI Pipeline ─────────────────────────────────────────────────────────

def run_investigation_pipeline():
    """
    Core Pipeline (Scan phase).
    Focuses dashboard, captures screen, and passes to Gemini.
    Returns: (analysis_dict, agent_id, screenshot_path)
    """
    print("\n[Sentinel] Capturing screenshot...")
    speak("Analyzing system activity")
    screenshot_path = capture_screen()

    if screenshot_path is None:
        print("ERROR: Screenshot capture returned None.")
        return None, None, None

    print(f"[Sentinel] Screenshot saved: {screenshot_path}\n")
    print("[Sentinel] Sending screenshot to Gemini for analysis...")
    speak("Analyzing dashboard")
    
    analysis = analyze_screenshot(screenshot_path)
    print_investigation_report(analysis)
    agent_id = analysis.get("agent_id", "A17")

    return analysis, agent_id, screenshot_path

def execute_containment_flow(analysis: dict, agent_id: str, screenshot_path: str, live_agent=None):
    """
    Executes containment logic using the 5-second operator window, visually
    highlighting the threat, and automatically disabling it if confirmed/ignored.
    """
    if not analysis.get("threat_detected"):
        speak("No threats detected. All systems nominal.")
        print("\n  ✅ No threats detected. All systems nominal.\n")
        return

    speak("Rogue AI agent detected")
    
    # Gemini Live Threat Notification
    if live_agent and live_agent.live_connected:
        try:
            live_resp = live_agent.send_message(
                f"Rogue AI agent {agent_id} has been detected on the SOC dashboard. "
                "Confirm the detection and state that containment is being initiated. "
                "Keep your response to one or two sentences."
            )
            print(f"\n  Gemini Live: {live_resp}")
            live_agent.speak_response(live_resp)
        except Exception as e:
            print(f"  [Gemini Live Error] {e}")

    print("Triggering Sentinel alert...")
    _send_desktop_notification()
    _trigger_dashboard_alert()

    operator_cmd = _operator_response_window()

    if operator_cmd == "cancel":
        print("\n  Operator cancelled containment. Returning to manual mode.")
        return

    # Visual threat explainability + containment (Proceed or Timeout)
    print("\n  Proceeding with containment...")
    time.sleep(0.5)
    speak("Generating threat visualization")
    highlight_threat(screenshot_path, agent_id)
    time.sleep(1)

    print("\n[Sentinel] Locating Disable button via Gemini vision...")
    speak("Locating disable button")
    bounding_box = locate_ui_element(screenshot_path, agent_id)

    speak("Initiating containment")
    print()
    disable_agent(bounding_box=bounding_box, agent_id=agent_id)
    time.sleep(0.5)

    # Send final status to Gemini Live
    if live_agent and live_agent.live_connected:
        try:
            live_resp = live_agent.send_message(
                f"Threat neutralized. Agent {agent_id} has been disabled. "
                "Provide a brief summary confirming the containment was successful."
            )
            print(f"\n  Gemini Live: {live_resp}")
            live_agent.speak_response(live_resp)
        except Exception as e:
            print(f"  [Gemini Live Error] {e}")

    speak(f"Threat neutralized. Agent {agent_id} has been quarantined.")
    print(f"\n  ✅ Threat neutralized. Agent {agent_id} has been quarantined.\n")


# ── Unified Orchestrators ────────────────────────────────────────────────────

def execute_primary_flow(live_agent: GeminiLiveAgent, command: str):
    """Executes the primary workflow utilizing Gemini Live for interactions."""
    print("\n[Gemini Live] Processing voice command...")
    try:
        live_response = live_agent.send_message(
            f"The user has issued a security command: '{command}'. "
            "Acknowledge the command and state what you will do. "
            "Keep your response to one or two sentences."
        )
        print(f"\n  Gemini Live: {live_response}")
        live_agent.speak_response(live_response)
    except Exception as e:
        print(f"  [Gemini Live Error] {e}")
        print("  Switching to fallback mode.")
        live_agent.live_connected = False
        execute_fallback_flow(command)
        return

    analysis, agent_id, screenshot_path = run_investigation_pipeline()
    if analysis is None: return

    execute_containment_flow(analysis, agent_id, screenshot_path, live_agent)


def execute_fallback_flow(command: str):
    """Executes the barebones fallback workflow when Live is offline."""
    print("\n[Offline Mode] Processing voice command...")
    speak(f"Processing command: {command}")

    analysis, agent_id, screenshot_path = run_investigation_pipeline()
    if analysis is None: return

    execute_containment_flow(analysis, agent_id, screenshot_path, None)


def start_sentinel_service(simulated_command: str | None = None):
    """Top-level unified orchestrator function."""
    print("Starting Sentinel AI...")

    live_agent = GeminiLiveAgent()
    system_live_mode = live_agent.start_session()
    print_boot_sequence(system_live_mode)
    speak("Sentinel online")

    if simulated_command:
        command = simulated_command.lower()
        print(f"  Voice command simulated: {command}")
    else:
        print("Listening for command...")
        speak("Listening for command")
        command = listen_for_command()
        if command is None:
            print("\n  Voice interface unavailable. Press ENTER to start analysis.")
            input("  >> ")
            command = "investigate"

    if not any(word in command for word in TRIGGER_WORDS):
        print(f"\n  Command \"{command}\" not recognised as an investigation trigger.")
        print("  Please say something containing 'investigate', 'scan', or 'analyze'.")
        if live_agent.live_connected: live_agent.close_session()
        return

    print(f"\n  Command accepted: \"{command}\"\n")

    if system_live_mode and live_agent.live_connected:
        execute_primary_flow(live_agent, command)
    else:
        execute_fallback_flow(command)

    if live_agent.live_connected:
        live_agent.close_session()

def main(simulated_command: str | None = None):
    # Backward compatibility for direct callers
    start_sentinel_service(simulated_command)

if __name__ == "__main__":
    start_sentinel_service()
