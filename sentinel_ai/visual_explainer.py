"""
Visual Explainer Module
-----------------------
Creates an annotated version of the SOC dashboard screenshot
that highlights the detected rogue agent with a red bounding
box and threat label, then opens the image for the user to see.
"""

import os
from PIL import Image, ImageDraw, ImageFont


# ── Region Configuration ────────────────────────────────────────────────────
# Approximate bounding-box for the Agents table on the SOC dashboard
# running at http://localhost:3000 on a 1920×1080 display.
#
# ⚠️  Adjust these if your screen resolution or browser layout differs.
#     The values represent (left, top, right, bottom) in pixels.

AGENT_TABLE_REGION = (350, 680, 1410, 830)

# Label position: just above the top-left corner of the box
LABEL_OFFSET_Y = 30  # pixels above the rectangle


def highlight_threat(
    image_path: str,
    agent_id: str = "A17",
    output_filename: str = "annotated_screenshot.png",
) -> str:
    """
    Load a screenshot, draw a red rectangle around the agent table
    region, overlay a threat label, save and open the annotated image.

    Args:
        image_path:      Path to the original screenshot PNG.
        agent_id:        The rogue agent identifier (e.g. "A17").
        output_filename: Name of the annotated output file.

    Returns:
        The absolute path to the saved annotated image.
    """
    # ── Load the screenshot ──────────────────────────────────────────────
    img = Image.open(image_path).convert("RGBA")
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    # ── Draw a semi-transparent red fill inside the region ───────────────
    left, top, right, bottom = AGENT_TABLE_REGION
    draw.rectangle(
        [left, top, right, bottom],
        fill=(255, 0, 0, 40),          # subtle red wash
        outline=(255, 0, 0, 255),      # solid red border
        width=3,
    )

    # ── Compose overlay onto original ────────────────────────────────────
    annotated = Image.alpha_composite(img, overlay)
    annotated = annotated.convert("RGB")

    # ── Draw the threat label ────────────────────────────────────────────
    label_draw = ImageDraw.Draw(annotated)
    label_text = f"⚠ Threat Detected: Agent {agent_id}"

    # Try to use a larger built-in font; fall back to default if unavailable
    try:
        font = ImageFont.truetype("arial.ttf", 28)
    except (IOError, OSError):
        try:
            font = ImageFont.truetype("DejaVuSans-Bold.ttf", 28)
        except (IOError, OSError):
            font = ImageFont.load_default()

    label_x = left
    label_y = top - LABEL_OFFSET_Y - 10

    # Background rectangle behind the label for readability
    bbox = label_draw.textbbox((label_x, label_y), label_text, font=font)
    padding = 6
    label_draw.rectangle(
        [bbox[0] - padding, bbox[1] - padding,
         bbox[2] + padding, bbox[3] + padding],
        fill=(180, 0, 0),
    )
    label_draw.text((label_x, label_y), label_text, fill="white", font=font)

    # ── Save the annotated image ─────────────────────────────────────────
    save_dir = os.path.dirname(os.path.abspath(image_path))
    output_path = os.path.join(save_dir, output_filename)
    annotated.save(output_path)
    print(f"\n  Threat visualization generated: {output_path}")

    # ── Open the image so the user can see it ────────────────────────────
    try:
        os.startfile(output_path)  # Windows-specific
    except AttributeError:
        # Fallback for non-Windows platforms
        import subprocess
        subprocess.Popen(["xdg-open", output_path])

    return output_path
