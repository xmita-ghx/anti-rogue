"""
Voice Interface Module
----------------------
Provides voice command input (SpeechRecognition) and
text-to-speech output (pyttsx3) for the Sentinel AI agent.
"""

import pyttsx3
import speech_recognition as sr


def speak(text: str) -> None:
    """
    Convert text to speech using the pyttsx3 offline TTS engine.

    A fresh engine instance is created each call to avoid
    COM-threading issues on Windows.

    Args:
        text: The string to speak aloud.
    """
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print(f"  [TTS Error] Could not speak: {e}")


def listen_for_command(timeout: int = 5, phrase_limit: int = 8) -> str | None:
    """
    Listen for a voice command through the default microphone.

    Uses the Google Web Speech API (via SpeechRecognition) for
    speech-to-text conversion.

    Args:
        timeout:       Max seconds to wait for speech to begin.
        phrase_limit:   Max seconds of speech to capture.

    Returns:
        The recognised command string (lowercase), or None if
        recognition fails or no microphone is available.
    """
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("  Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            print("  Listening...")
            audio = recognizer.listen(
                source, timeout=timeout, phrase_time_limit=phrase_limit
            )
    except OSError:
        # No microphone found
        return None
    except sr.WaitTimeoutError:
        print("  No speech detected within timeout.")
        return None
    except Exception as e:
        print(f"  [Microphone Error] {e}")
        return None

    # Attempt recognition
    try:
        command = recognizer.recognize_google(audio)
        print(f"  Recognised: \"{command}\"")
        return command.lower()
    except sr.UnknownValueError:
        print("  Could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"  [Recognition Error] {e}")
        return None
