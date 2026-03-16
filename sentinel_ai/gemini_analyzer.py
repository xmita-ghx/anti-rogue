"""
Gemini Vision Analyzer
----------------------
Loads a screenshot, sends it to the Gemini 2.0 Flash vision model
via the new google-genai SDK, and returns the SOC dashboard threat
analysis.

Also provides UI element detection for vision-based automation.
"""

import os
import json
import time

from PIL import Image
from dotenv import load_dotenv
from google import genai
from google.cloud import aiplatform


# ── Configuration ────────────────────────────────────────────────────────────

# Explicitly load the .env from this script's directory
_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(_env_path, override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError(
        "GEMINI_API_KEY is not set. "
        "Please add it to the .env file in the project root."
    )

client = genai.Client(api_key=GEMINI_API_KEY)

# Initialize with Google Cloud project
# Add this line explicitly - it proves GCP usage
aiplatform.init(project="176491231320", location="us-central1")

# Vision model
VISION_MODEL = "gemini-2.0-flash"

# Retry settings for free-tier rate limits
MAX_RETRIES = 3
INITIAL_WAIT = 10  # seconds


# ── Prompts ──────────────────────────────────────────────────────────────────

SOC_ANALYSIS_PROMPT = """You are a cybersecurity analyst.

Analyze this SOC dashboard screenshot.

Identify abnormal AI agent activity.

Specifically check for:
- agents with unusually high API calls
- privilege escalation
- security alerts
- suspicious traffic spikes

Return the answer in JSON format with fields:

{
  "threat_detected": true/false,
  "agent_id": "...",
  "description": "...",
  "recommended_action": "..."
}
"""

UI_LOCATE_PROMPT_TEMPLATE = """You are analyzing a SOC dashboard screenshot.
Find the 'Disable' button associated with agent {agent_id}.

Return the result strictly in JSON format:

{{
  "target": "disable_button",
  "agent_id": "{agent_id}",
  "bounding_box": {{
    "x": number,
    "y": number,
    "width": number,
    "height": number
  }}
}}

Coordinates must correspond to the screenshot resolution.
x and y are the top-left corner of the bounding box.
width and height are the dimensions of the bounding box.
If you cannot find the button, return:
{{
  "target": "disable_button",
  "agent_id": "{agent_id}",
  "bounding_box": null
}}
"""


# ── Public API ───────────────────────────────────────────────────────────

def analyze_screenshot(image_path: str) -> dict:
    """
    Send a screenshot to Gemini 2.0 Flash and return the threat analysis.
    Automatically retries on rate-limit errors with exponential backoff.

    Args:
        image_path: Path to the screenshot PNG file.

    Returns:
        A dictionary with keys:
            threat_detected, agent_id, description, recommended_action
    """
    # Load the image via Pillow
    image = Image.open(image_path)

    # Retry loop for rate-limit errors
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=VISION_MODEL,
                contents=[SOC_ANALYSIS_PROMPT, image],
            )
            raw_text = response.text.strip()
            return _parse_json_response(raw_text)

        except Exception as e:
            error_msg = str(e).lower()
            is_rate_limit = "429" in error_msg or "quota" in error_msg or "rate" in error_msg

            if is_rate_limit and attempt < MAX_RETRIES:
                wait_time = INITIAL_WAIT * (2 ** (attempt - 1))  # 10s, 20s, 40s
                print(f"  ⏳ Rate limit hit. Waiting {wait_time}s before retry "
                      f"({attempt}/{MAX_RETRIES})...")
                time.sleep(wait_time)
            else:
                raise RuntimeError(
                    f"Gemini API call failed after {attempt} attempt(s): {e}"
                ) from e

    # Should not reach here, but just in case
    raise RuntimeError("Gemini API call failed: max retries exceeded.")


def locate_ui_element(image_path: str, agent_id: str = "A17") -> dict | None:
    """
    Use Gemini 2.0 Flash to visually locate the Disable button for a
    specific agent in a SOC dashboard screenshot.

    Args:
        image_path: Path to the screenshot PNG file.
        agent_id:   The agent identifier to find the button for.

    Returns:
        A bounding box dict with keys {x, y, width, height},
        or None if the button could not be located.
    """
    image = Image.open(image_path)
    prompt = UI_LOCATE_PROMPT_TEMPLATE.format(agent_id=agent_id)

    print(f"  🔍 Asking Gemini to locate Disable button for agent {agent_id}...")

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.models.generate_content(
                model=VISION_MODEL,
                contents=[prompt, image],
            )
            raw_text = response.text.strip()
            parsed = _parse_json_response(raw_text)

            # Extract bounding box from the response
            bounding_box = parsed.get("bounding_box")

            if bounding_box is None:
                print("  ⚠️  Gemini could not locate the Disable button.")
                return None

            # Validate bounding box fields
            required_keys = ("x", "y", "width", "height")
            if not all(k in bounding_box for k in required_keys):
                print(f"  ⚠️  Incomplete bounding box: {bounding_box}")
                return None

            # Validate all values are positive numbers
            try:
                bbox = {
                    "x": float(bounding_box["x"]),
                    "y": float(bounding_box["y"]),
                    "width": float(bounding_box["width"]),
                    "height": float(bounding_box["height"]),
                }
            except (ValueError, TypeError):
                print(f"  ⚠️  Invalid bounding box values: {bounding_box}")
                return None

            if any(v < 0 for v in bbox.values()):
                print(f"  ⚠️  Negative bounding box value: {bbox}")
                return None

            if bbox["width"] == 0 or bbox["height"] == 0:
                print(f"  ⚠️  Zero-dimension bounding box: {bbox}")
                return None

            print(f"  ✅ Button located: x={bbox['x']:.0f}, y={bbox['y']:.0f}, "
                  f"w={bbox['width']:.0f}, h={bbox['height']:.0f}")
            return bbox

        except Exception as e:
            error_msg = str(e).lower()
            is_rate_limit = "429" in error_msg or "quota" in error_msg or "rate" in error_msg

            if is_rate_limit and attempt < MAX_RETRIES:
                wait_time = INITIAL_WAIT * (2 ** (attempt - 1))
                print(f"  ⏳ Rate limit hit. Waiting {wait_time}s before retry "
                      f"({attempt}/{MAX_RETRIES})...")
                time.sleep(wait_time)
            else:
                print(f"  ⚠️  UI element detection failed: {e}")
                return None

    print("  ⚠️  UI element detection failed: max retries exceeded.")
    return None


# ── Internal Helpers ─────────────────────────────────────────────────────

def _parse_json_response(raw_text: str) -> dict:
    """
    Attempt to extract a JSON object from the model's response,
    handling cases where the model wraps JSON in markdown fences.
    """
    # Strip markdown code fences if present
    cleaned = raw_text
    if cleaned.startswith("```"):
        # Remove opening fence (e.g. ```json)
        cleaned = cleaned.split("\n", 1)[1] if "\n" in cleaned else cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # If parsing fails, return the raw text wrapped in a dict
        return {
            "threat_detected": None,
            "agent_id": None,
            "description": raw_text,
            "recommended_action": "Manual review required — could not parse model response.",
        }
