"""
Desktop Controller Module
--------------------------
Automates mouse-driven interaction with the SOC dashboard
to disable a rogue agent.

This module now relies entirely on vision-based targeting
provided by the Gemini API. Hardcoded coordinates have 
been eliminated to ensure stability across different screen
resolutions and layouts.
"""

import time
import pyautogui

# Safety: allow the user to abort by moving mouse to a corner
pyautogui.FAILSAFE = True

# ── Screen Bounds (basic sanity check) ───────────────────────────────────

SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()


# ── Vision-Based Click ───────────────────────────────────────────────────

def disable_agent_vision(bounding_box: dict, agent_id: str = "A17"):
    """
    Click the Disable button using Gemini-detected bounding box coordinates.

    Args:
        bounding_box: Dict with keys {x, y, width, height} from Gemini.
        agent_id:     The agent identifier being disabled.
    """
    x = bounding_box["x"]
    y = bounding_box["y"]
    width = bounding_box["width"]
    height = bounding_box["height"]

    # Calculate center of the bounding box
    center_x = x + width / 2
    center_y = y + height / 2

    # Clamp to screen bounds
    center_x = max(0, min(center_x, SCREEN_WIDTH - 1))
    center_y = max(0, min(center_y, SCREEN_HEIGHT - 1))

    print(f"  🎯 Vision target: ({center_x:.0f}, {center_y:.0f})")
    print(f"  Moving to Disable button for {agent_id}...")

    pyautogui.moveTo(center_x, center_y, duration=0.5)
    time.sleep(0.3)

    print(f"  Clicking Disable...")
    pyautogui.click()
    time.sleep(1)

    print(f"  ✅ Agent {agent_id} disabled successfully (vision-based).")


# ── Orchestrator ─────────────────────────────────────────────────────────

def disable_agent(bounding_box: dict | None = None, agent_id: str = "A17"):
    """
    Disable a rogue agent on the SOC dashboard.

    Relies purely on vision-based clicking. If the bounding box is None or
    invalid, it logs a clear error and aborts to prevent unsafe random clicking.

    Args:
        bounding_box: Bounding box from Gemini vision (or None).
        agent_id:     The agent identifier to disable.
    """
    print("Initiating automated containment...")
    time.sleep(0.3)

    if bounding_box is not None and _is_valid_bbox(bounding_box):
        print(f"  Using Gemini vision-based navigation for {agent_id}.")
        disable_agent_vision(bounding_box, agent_id)
    else:
        print(f"  ⚠️  Containment Aborted: Accurate UI localization failed for agent {agent_id}.")
        print("  Sentinel will NOT attempt a blind click for safety reasons.")
        print("  Manual intervention required.")


def _is_valid_bbox(bbox: dict) -> bool:
    """
    Validate that a bounding box dict has the required keys with
    positive numeric values within screen bounds.
    """
    required = ("x", "y", "width", "height")

    if not all(k in bbox for k in required):
        return False

    try:
        x = float(bbox["x"])
        y = float(bbox["y"])
        w = float(bbox["width"])
        h = float(bbox["height"])
    except (ValueError, TypeError):
        return False

    if w <= 0 or h <= 0:
        return False

    # Check that center point is within screen bounds
    cx = x + w / 2
    cy = y + h / 2

    if cx < 0 or cx >= SCREEN_WIDTH or cy < 0 or cy >= SCREEN_HEIGHT:
        return False

    return True
