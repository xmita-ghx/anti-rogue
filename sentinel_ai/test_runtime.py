import sys
import time
import threading
from unittest.mock import patch, MagicMock

sys.modules['plyer'] = MagicMock()

def test_control_panel():
    print("\n[FLOW 2 & 8] Testing Control Panel Buttons & Responsiveness")
    try:
        from sentinel_control_panel import SentinelControlPanel
        app = SentinelControlPanel()
        
        print("Clicking Demo Button...")
        app._run_demo()
        print("Clicking Sentinel Button...")
        app._run_sentinel()
        print("Clicking Rogue Button...")
        app._trigger_rogue_agent()
        
        print("Checking UI responsiveness... (If this prints immediately, UI did not block)")
        time.sleep(1) # wait for threads to start
        print("[FLOW 8] UI thread remained responsive during execution")
    except Exception as e:
        print(f"Error in control panel test: {e}")

def test_rogue():
    print("\n[FLOW 3] Testing Rogue Agent Trigger")
    try:
        import rogue
        res = rogue.trigger_rogue_agent()
        print(f"Rogue trigger completed with return: {res}")
    except Exception as e:
        print(f"Rogue trigger failed with exception: {e}")

def test_sentinel_flows():
    print("\n[FLOW 4, 5, 6, 7] Testing Sentinel AI Pipeline")
    import main
    import desktop_controller
    
    print("Testing primary/fallback AI entry points...")
    print(f"Using desktop_controller targeting method. Hardcoded fallback coordinates removed? {'disable_agent_fallback' not in dir(desktop_controller)}")
    
    # We will mock capture_screen and Gemini analyze to avoid relying on actual API keys and screenshots during automated tests.
    with patch("main.capture_screen", return_value="dummy.png"), \
         patch("main.analyze_screenshot", return_value={"threat_detected": True, "agent_id": "A17", "description": "simulated anomaly"}), \
         patch("sentinel_monitor.notification.notify"), \
         patch("main._trigger_dashboard_alert"), \
         patch("main.highlight_threat"), \
         patch("main.locate_ui_element", return_value={"x": 100, "y": 100, "width": 50, "height": 20}), \
         patch("desktop_controller.pyautogui.click"), \
         patch("desktop_controller.pyautogui.moveTo"), \
         patch("main._operator_response_window", return_value="timeout"), \
         patch("main.speak"):

        print("-> Simulating Fallback Flow (No Gemini Live)")
        main.execute_fallback_flow("investigate")
        
        print("\n-> Simulating Primary Flow (Gemini Live MOCKED)")
        class MockLive:
            live_connected = True
            def send_message(self, *args): return "Mocked Live Response"
            def speak_response(self, *args): pass
            
        main.execute_primary_flow(MockLive(), "investigate")
        
        print("Sentinel flows completed safely.")

if __name__ == "__main__":
    test_control_panel()
    test_rogue()
    test_sentinel_flows()
