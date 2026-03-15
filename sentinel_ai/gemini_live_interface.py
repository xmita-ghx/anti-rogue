"""
Gemini Live Interface Module
-----------------------------
Provides the GeminiLiveAgent class that maintains a real-time
conversational session with the Gemini Live API, enabling the
Sentinel AI system to send text messages and receive streaming
text responses which are spoken aloud via pyttsx3.

When the Live session is unavailable, the agent falls back to
standard generate_content calls for non-realtime responses.

Uses the google-genai SDK exclusively.
"""

import os
import asyncio

from dotenv import load_dotenv
from google import genai
from google.genai import types
import pyttsx3


# ── Configuration ────────────────────────────────────────────────────────────

_env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
load_dotenv(_env_path, override=True)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise EnvironmentError(
        "GEMINI_API_KEY is not set. "
        "Please add it to the .env file in the project root."
    )

# Models
LIVE_MODEL = "gemini-2.0-flash-live"
FALLBACK_MODEL = "gemini-2.0-flash"

SYSTEM_INSTRUCTION = (
    "You are Sentinel, a concise AI cybersecurity assistant. "
    "You help monitor SOC dashboards, detect rogue AI agents, "
    "and coordinate automated threat containment. "
    "Keep your responses brief and action-oriented."
)


# ── GeminiLiveAgent ──────────────────────────────────────────────────────────

class GeminiLiveAgent:
    """
    Manages a Gemini Live API session for real-time text conversations.

    Attributes:
        live_connected (bool): True if the Live session is active and
                               responding, False otherwise.

    Usage (synchronous wrapper):
        agent = GeminiLiveAgent()
        connected = agent.start_session()   # opens the live connection
        response = agent.send_message("Sentinel investigate the system")
        agent.speak_response(response)
        agent.close_session()
    """

    def __init__(self):
        self._client = genai.Client(api_key=GEMINI_API_KEY)
        self._session = None
        self._loop = None
        self.live_connected = False

    # ── Session lifecycle ────────────────────────────────────────────────

    def start_session(self) -> bool:
        """
        Attempt to open a Gemini Live session.

        Returns:
            True if the session connected successfully, False otherwise.
        """
        try:
            self._loop = asyncio.new_event_loop()
            self._session = self._loop.run_until_complete(self._connect())
            self.live_connected = True
        except Exception as e:
            print(f"  Gemini Live connection failed: {e}")
            print("  Switching to fallback mode.")
            self.live_connected = False
            if self._loop:
                self._loop.close()
                self._loop = None

        return self.live_connected

    async def _connect(self):
        """Internal: establish the async live connection."""
        config = {
            "response_modalities": ["TEXT"],
            "system_instruction": SYSTEM_INSTRUCTION,
        }
        session = self._client.aio.live.connect(
            model=LIVE_MODEL,
            config=config,
        )
        return await session.__aenter__()

    def close_session(self) -> None:
        """Tear down the Gemini Live session."""
        if self._session:
            try:
                self._loop.run_until_complete(self._session.close())
            except Exception:
                pass
            self._session = None
        if self._loop:
            self._loop.close()
            self._loop = None
        self.live_connected = False
        print("  Gemini Live session closed.")

    # ── Heartbeat ────────────────────────────────────────────────────────

    def check_live_status(self) -> bool:
        """
        Verify the Gemini Live session is alive by sending a short
        ping message and checking for a response.

        Returns:
            True if the session responds, False otherwise.
        """
        if not self._session or not self._loop:
            print("  Gemini Live session inactive.")
            self.live_connected = False
            return False

        try:
            response = self._loop.run_until_complete(
                self._async_send("ping")
            )
            if response:
                print("  Gemini Live responding.")
                self.live_connected = True
                return True
            else:
                print("  Gemini Live session inactive.")
                self.live_connected = False
                return False
        except Exception:
            print("  Gemini Live session inactive.")
            self.live_connected = False
            return False

    # ── Messaging ────────────────────────────────────────────────────────

    def send_message(self, text: str) -> str:
        """
        Send a text message to Gemini and collect the response.

        If the Live session is active, uses the streaming Live API.
        Otherwise, falls back to a standard generate_content call.

        Args:
            text: The user message to send.

        Returns:
            The complete response string from Gemini.
        """
        # Try Live session first
        if self._session and self.live_connected and self._loop:
            try:
                return self._loop.run_until_complete(self._async_send(text))
            except Exception as e:
                print(f"  [Gemini Live Error] {e}")
                print("  Falling back to standard generation.")
                self.live_connected = False

        # Fallback: standard (non-Live) generation
        return self._fallback_generate(text)

    def _fallback_generate(self, text: str) -> str:
        """
        Standard (non-realtime) Gemini text generation as fallback.
        """
        try:
            response = self._client.models.generate_content(
                model=FALLBACK_MODEL,
                contents=text,
            )
            return response.text
        except Exception as e:
            return f"[Gemini Error] {e}"

    async def _async_send(self, text: str) -> str:
        """Internal: send content via Live session and collect response."""
        await self._session.send_client_content(
            turns=types.Content(
                role="user",
                parts=[types.Part(text=text)],
            ),
            turn_complete=True,
        )

        full_response = []
        async for msg in self._session.receive():
            if msg.text:
                full_response.append(msg.text)

        return "".join(full_response)

    # ── Text-to-speech ───────────────────────────────────────────────────

    @staticmethod
    def speak_response(text: str) -> None:
        """
        Speak the given text aloud using pyttsx3.

        Args:
            text: The text to speak.
        """
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
            engine.stop()
        except Exception as e:
            print(f"  [TTS Error] {e}")
