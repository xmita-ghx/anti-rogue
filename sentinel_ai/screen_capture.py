"""
Screen Capture Module
---------------------
Captures the entire desktop screen using pyautogui and saves
the screenshot locally as a PNG file.
"""

import os
import pyautogui


def capture_screen(filename: str = "screenshot.png") -> str | None:
    """
    Capture the entire desktop screen and save it as a PNG image.

    Args:
        filename: Name of the output file (default: "screenshot.png").

    Returns:
        The absolute file path of the saved screenshot.
    """
    screenshot = pyautogui.screenshot()

    if screenshot is None:
        print("  [Sentinel] Screenshot capture failed — pyautogui returned None.")
        return None

    # Resolve to an absolute path relative to this script's directory
    save_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(save_dir, filename)

    screenshot.save(filepath)
    return filepath
