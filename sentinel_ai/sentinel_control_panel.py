"""
Sentinel AI — Digital SOC Control Console
=========================================
Dark-themed Tkinter UI for monitoring the SOC environment
and launching Sentinel AI containment measures.

Provides:
- Live parsing of dashboard state using background monitoring.
- Demo sequence.
- Rogue Agent Injection.
- Sentinel AI autonomous launch.
"""

import os
import sys
import time
import threading
import tkinter as tk
from tkinter import scrolledtext
from datetime import datetime

import pyautogui

# For OCR parsing of the dashboard
try:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

# ── Path Safety ──────────────────────────────────────────────────────────────

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(_SCRIPT_DIR)
if _SCRIPT_DIR not in sys.path:
    sys.path.insert(0, _SCRIPT_DIR)

# ── Theme Constants ──────────────────────────────────────────────────────────

BG        = "#0f172a"
PANEL     = "#1e293b"
TEXT      = "#e2e8f0"
DIM_TEXT  = "#94a3b8"
GREEN     = "#22c55e"
RED       = "#ef4444"
AMBER     = "#f59e0b"
ACCENT    = "#38bdf8"
BORDER    = "#334155"
BTN_BG    = "#334155"
BTN_HOVER = "#475569"
RED_BG    = "#7f1d1d"
RED_HOVER = "#991b1b"


# ── Application ──────────────────────────────────────────────────────────────

class SentinelControlPanel:
    """Tkinter GUI for the Sentinel AI Digital Console."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sentinel AI Digital Console")
        self.root.geometry("900x550")
        self.root.configure(bg=BG)
        self.root.resizable(False, False)

        # ── State ────────────────────────────────────────────────────────
        self.monitoring_status = tk.StringVar(value="Standby")
        self.threat_level = tk.StringVar(value="Normal")
        self.ai_mode = tk.StringVar(value="Offline")

        self._stop_background_sync = False

        self._build_ui()
        self.log_message("Sentinel AI Digital Console initialized.")
        
        # Start background sync if OCR is available
        if OCR_AVAILABLE:
            self._start_dashboard_sync()
        else:
            self.log_message("Live dashboard sync disabled (OCR unavailable).", "warning")

    # ── UI Construction ──────────────────────────────────────────────────

    def _build_ui(self):
        self._build_header()

        mid_frame = tk.Frame(self.root, bg=BG)
        mid_frame.pack(fill="x", padx=16, pady=(8, 4))

        self._build_status_panel(mid_frame)
        self._build_control_buttons(mid_frame)

        self._build_log_panel()

    def _build_header(self):
        header = tk.Frame(self.root, bg=PANEL, pady=14)
        header.pack(fill="x")

        tk.Label(
            header,
            text="◈  SENTINEL CYBER DEFENSE CONSOLE",
            font=("Consolas", 18, "bold"),
            fg=ACCENT, bg=PANEL,
        ).pack()

        tk.Label(
            header,
            text="Autonomous SOC Orchestrator",
            font=("Consolas", 10),
            fg=DIM_TEXT, bg=PANEL,
        ).pack(pady=(2, 0))

    def _build_status_panel(self, parent):
        frame = tk.LabelFrame(
            parent, text="  LIVE SOC STATUS  ",
            font=("Consolas", 10, "bold"),
            fg=DIM_TEXT, bg=PANEL,
            bd=1, relief="groove",
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=16, pady=12,
        )
        frame.pack(side="left", fill="both", expand=True, padx=(0, 8))

        indicators = [
            ("Sentinel State", self.monitoring_status),
            ("Dashboard Threat", self.threat_level),
            ("AI Containment", self.ai_mode),
        ]

        for label_text, var in indicators:
            row = tk.Frame(frame, bg=PANEL)
            row.pack(fill="x", pady=8)

            tk.Label(
                row, text=f"{label_text}:",
                font=("Consolas", 12),
                fg=DIM_TEXT, bg=PANEL, width=16, anchor="w",
            ).pack(side="left")

            lbl = tk.Label(
                row, textvariable=var,
                font=("Consolas", 12, "bold"),
                fg=GREEN, bg=PANEL,
            )
            lbl.pack(side="left", padx=(4, 0))

            var.trace_add("write", lambda *_, v=var, l=lbl: self._color_indicator(v, l))
            self._color_indicator(var, lbl)

    def _color_indicator(self, var, label):
        """Set indicator color based on value."""
        val = var.get().lower()
        if val in ("critical", "containment active", "active"):
            label.configure(fg=RED)
        elif val in ("elevated", "investigating", "syncing"):
            label.configure(fg=AMBER)
        else:
            label.configure(fg=GREEN)

    def _build_control_buttons(self, parent):
        frame = tk.LabelFrame(
            parent, text="  OPERATOR CONTROLS  ",
            font=("Consolas", 10, "bold"),
            fg=DIM_TEXT, bg=PANEL,
            bd=1, relief="groove",
            highlightbackground=BORDER,
            highlightthickness=1,
            padx=16, pady=12,
        )
        frame.pack(side="right", fill="both", padx=(8, 0))

        # ── Buttons: Demo, Trigger Rogue, Start Sentinel ──────────────
        buttons = [
            ("▶  Run Full Demo", self._run_demo, GREEN),
            ("🛡  Start Sentinel Agent", self._run_sentinel, ACCENT),
        ]

        for text, cmd, color in buttons:
            btn = tk.Button(
                frame, text=text,
                font=("Consolas", 11, "bold"),
                fg=color, bg=BTN_BG,
                activeforeground=color, activebackground=BTN_HOVER,
                bd=0, relief="flat",
                cursor="hand2",
                width=26, pady=6,
                command=cmd,
            )
            btn.pack(pady=4)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg=BTN_HOVER))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg=BTN_BG))

        sep = tk.Frame(frame, bg=BORDER, height=1)
        sep.pack(fill="x", pady=6)

        rogue_btn = tk.Button(
            frame, text="⚠  Trigger Rogue Agent",
            font=("Consolas", 11, "bold"),
            fg="#fca5a5", bg=RED_BG,
            activeforeground="#fca5a5", activebackground=RED_HOVER,
            bd=0, relief="flat",
            cursor="hand2",
            width=26, pady=6,
            command=self._trigger_rogue_agent,
        )
        rogue_btn.pack(pady=4)
        rogue_btn.bind("<Enter>", lambda e: rogue_btn.configure(bg=RED_HOVER))
        rogue_btn.bind("<Leave>", lambda e: rogue_btn.configure(bg=RED_BG))

    def _build_log_panel(self):
        frame = tk.LabelFrame(
            self.root, text="  SYSTEM LOG  ",
            font=("Consolas", 10, "bold"),
            fg=DIM_TEXT, bg=PANEL,
            bd=1, relief="groove",
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        frame.pack(fill="both", expand=True, padx=16, pady=(4, 12))

        self.log_text = scrolledtext.ScrolledText(
            frame,
            font=("Consolas", 10),
            fg=TEXT, bg=BG,
            insertbackground=TEXT,
            selectbackground=BORDER,
            bd=0, relief="flat",
            wrap="word",
            state="disabled",
            height=10,
        )
        self.log_text.pack(fill="both", expand=True, padx=4, pady=4)

        # Tag colors for log highlighting
        self.log_text.tag_configure("timestamp", foreground=DIM_TEXT)
        self.log_text.tag_configure("sentinel", foreground=ACCENT)
        self.log_text.tag_configure("error", foreground=RED)
        self.log_text.tag_configure("success", foreground=GREEN)
        self.log_text.tag_configure("warning", foreground=AMBER)

    # ── Background Dashboard Sync ────────────────────────────────────────

    def _start_dashboard_sync(self):
        """Periodically captures the screen and checks Threat Level."""
        def sync_task():
            while not self._stop_background_sync:
                # Do not sync if Sentinel or Demo is actively manipulating the dashboard
                if self.monitoring_status.get() != "Standby" and self.monitoring_status.get() != "Syncing":
                    time.sleep(2)
                    continue
                
                self.monitoring_status.set("Syncing")
                try:
                    screenshot = pyautogui.screenshot()
                    ocr_text = pytesseract.image_to_string(screenshot)
                    
                    if "CRITICAL" in ocr_text.upper():
                        self.threat_level.set("Critical")
                    elif "ELEVATED" in ocr_text.upper():
                        self.threat_level.set("Elevated")
                    elif hasattr(self, "threat_level_changed_manually"):
                        pass # Preserve if user clicked the trigger button
                    else:
                        self.threat_level.set("Normal")
                except Exception:
                    pass
                
                self.monitoring_status.set("Standby")
                time.sleep(5)  # Sync every 5 seconds securely
        
        threading.Thread(target=sync_task, daemon=True).start()

    # ── Logging ──────────────────────────────────────────────────────────

    def log_message(self, message: str, level: str = "info"):
        def _write():
            ts = datetime.now().strftime("%H:%M:%S")
            self.log_text.configure(state="normal")
            self.log_text.insert("end", f"[{ts}] ", "timestamp")
            tag = {"error": "error", "success": "success", "warning": "warning"}.get(level, "sentinel")
            self.log_text.insert("end", f"[Console] {message}\n", tag)
            self.log_text.see("end")
            self.log_text.configure(state="disabled")

        self.root.after(0, _write)

    # ── Mode Runners ─────────────────────────────────────────────────────

    def _run_in_thread(self, target, mode_name: str):
        def wrapper():
            self.log_message(f"Starting {mode_name}...")
            try:
                target()
                self.log_message(f"{mode_name} completed.", "success")
            except KeyboardInterrupt:
                self.log_message(f"{mode_name} interrupted by operator.", "warning")
            except Exception as e:
                self.log_message(f"Encountered an error during execution.", "error")
                self.log_message(f"Details: {e}", "error")
            finally:
                self.ai_mode.set("Offline")
                self.monitoring_status.set("Standby")

        threading.Thread(target=wrapper, daemon=True).start()

    def _run_demo(self):
        self.ai_mode.set("Investigating")
        self.monitoring_status.set("Active")
        
        def task():
            from demo import run_demo
            run_demo()

        self._run_in_thread(task, "Demo Mode")

    def _run_sentinel(self):
        self.ai_mode.set("Containment Active")
        self.monitoring_status.set("Active")

        def task():
            # Trigger the main Sentinel Loop (Voice Interface / Auto)
            from main import start_sentinel_service
            start_sentinel_service()

        self._run_in_thread(task, "Sentinel Defense Agent")

    def _trigger_rogue_agent(self):
        self.threat_level_changed_manually = True
        self.threat_level.set("Elevated")

        def task():
            from rogue import trigger_rogue_agent
            
            self.log_message("Triggering rogue agent scenario...")
            success = trigger_rogue_agent()
            
            if not success:
                self.log_message("Dashboard window not found or execution failed.", "error")
                self.threat_level.set("Normal")
                return

            self.threat_level.set("Critical")
            self.log_message("Rogue activity injected into dashboard.", "warning")

        self._run_in_thread(task, "Rogue Agent Injection")

    # ── Run ───────────────────────────────────────────────────────────────

    def run(self):
        self.root.mainloop()
        self._stop_background_sync = True


if __name__ == "__main__":
    app = SentinelControlPanel()
    app.run()
