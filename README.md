# 🛡️ Sentinel AI — Autonomous Rogue AI Agent Detector

> **Built for the Google Gemini API Developer Competition**

Sentinel AI is an autonomous cybersecurity system that monitors a live SOC (Security Operations Center) dashboard, detects rogue AI agents in real-time using **Gemini Vision**, and neutralizes threats — all without human intervention.

---

## 🎯 What It Does

1. **Monitors** a live SOC dashboard via screen capture and OCR
2. **Detects** rogue AI activity using Gemini 2.0 Flash Vision analysis
3. **Alerts** the operator with desktop notifications and dashboard warnings
4. **Waits 5 seconds** for a human response — if none, proceeds autonomously
5. **Locates** the Disable button dynamically using Gemini vision (no hardcoded coordinates)
6. **Neutralizes** the threat by clicking Disable on the dashboard automatically

---

## 🏗️ Architecture

```
demo.py (Single Entry Point)
  ├── SOC Dashboard (React app on localhost:3000)
  ├── Sentinel Control Panel (Tkinter GUI)
  │     ├── Run Full Demo
  │     ├── Start Sentinel Agent
  │     └── Trigger Rogue Agent
  ├── main.py (AI Orchestrator)
  │     ├── Primary Flow (Gemini Live + Voice)
  │     └── Fallback Flow (Offline mode)
  ├── rogue.py (Attack Simulator)
  ├── desktop_controller.py (Vision-based UI automation)
  ├── gemini_analyzer.py (Screenshot analysis via Gemini Vision)
  ├── gemini_live_interface.py (Real-time Gemini Live session)
  ├── sentinel_monitor.py (Continuous OCR monitoring)
  ├── screen_capture.py (Desktop screenshot utility)
  ├── voice_interface.py (Speech recognition + TTS)
  └── visual_explainer.py (Threat visualization overlay)
```

---

## 🤖 Gemini Models Used

| Model | Purpose |
|---|---|
| `gemini-2.0-flash-live` | Real-time voice conversation and live threat narration |
| `gemini-2.0-flash` | Vision analysis of dashboard screenshots + UI element localization + fallback text generation |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** (for the SOC dashboard)
- **Google Gemini API Key** ([Get one free](https://aistudio.google.com/app/apikey))
- **Tesseract OCR** (optional, for live dashboard sync)
- **Microphone** (for voice commands)

### 1. Clone the repo

```bash
git clone https://github.com/xmita-ghx/anti-rogue.git
cd anti-rogue
```

### 2. Install Python dependencies

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r sentinel_ai/requirements.txt
```

### 3. Set up your API key

Create `sentinel_ai/.env`:

```env
GEMINI_API_KEY=your_api_key_here
```

### 4. Start the SOC Dashboard

```bash
cd soc-dashboard
npm install
npm start
```

The dashboard will open at `http://localhost:3000`.

### 5. Launch Sentinel AI

In a **new terminal**:

```bash
cd sentinel_ai
python demo.py
```

---

## 🎮 How to Use

1. The **Sentinel Control Panel** will appear on screen
2. Click **"Trigger Rogue Agent"** → simulates a rogue AI attack on the dashboard
3. Click **"Start Sentinel Agent"** → Sentinel begins autonomous monitoring
4. Speak a command like *"Investigate"* or *"Scan"* into your microphone
5. Watch as Sentinel detects the threat, alerts you, waits 5 seconds, and disables the rogue agent automatically

---

## 📁 Project Structure

```
anti-rogue/
├── soc-dashboard/          # React SOC Dashboard (frontend)
│   ├── src/
│   │   ├── App.js          # Main dashboard with agent monitoring
│   │   └── components/     # Dashboard UI components
│   └── public/
│       └── index.html
├── sentinel_ai/            # Python AI Backend
│   ├── demo.py             # 🚀 Single entry point
│   ├── main.py             # AI orchestrator (primary + fallback)
│   ├── rogue.py            # Rogue agent attack simulator
│   ├── sentinel_control_panel.py  # Tkinter GUI console
│   ├── sentinel_monitor.py # Continuous OCR monitor
│   ├── desktop_controller.py     # Vision-based mouse automation
│   ├── gemini_analyzer.py  # Gemini Vision screenshot analysis
│   ├── gemini_live_interface.py  # Gemini Live real-time session
│   ├── screen_capture.py   # Screenshot capture utility
│   ├── voice_interface.py  # Speech recognition + TTS
│   ├── visual_explainer.py # Threat visualization overlay
│   └── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

---

## 🔑 Key Features

- **Zero hardcoded coordinates** — Disable button targeting is 100% vision-based via Gemini
- **Automatic fallback** — If Gemini Live drops, the system seamlessly switches to offline mode
- **Threaded UI** — Control panel never freezes during AI operations
- **5-second operator window** — Gives humans a chance to intervene before autonomous action
- **Graceful degradation** — Missing dependencies (OCR, voice) don't crash the system

---

## ⚙️ Tech Stack

| Layer | Technology |
|---|---|
| AI Vision | Google Gemini 2.0 Flash |
| Real-time AI | Google Gemini 2.0 Flash Live |
| Frontend | React, TailwindCSS, Chart.js |
| Backend | Python 3.10 |
| Automation | PyAutoGUI, PyGetWindow |
| Voice | SpeechRecognition, pyttsx3 |
| OCR | Tesseract (pytesseract) |
| Notifications | plyer |

---

## 📜 License

Built for the **Google Gemini API Developer Competition 2026**.
