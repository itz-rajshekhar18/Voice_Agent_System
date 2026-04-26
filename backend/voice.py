"""
voice.py — Voice interface layer.

  listen()  → records from microphone and returns transcribed text (str | None)
  speak()   → converts text to audible speech

STT: uses the SpeechRecognition library (Google Web Speech API by default).
TTS: uses pyttsx3 (offline, cross-platform) with a gTTS fallback for richer voices.

Both components are optional and degrade gracefully:
  - If microphone/audio is unavailable, listen() returns None.
  - If TTS fails, speak() silently logs the error and continues.
"""

import sys
import logging

logger = logging.getLogger(__name__)

# ── optional imports ──────────────────────────────────────────────────── #
try:
    import speech_recognition as sr
    _SR_AVAILABLE = True
except ImportError:
    _SR_AVAILABLE = False
    logger.warning("SpeechRecognition not installed. Voice input disabled.")

try:
    import pyttsx3
    _PYTTSX3_AVAILABLE = True
except ImportError:
    _PYTTSX3_AVAILABLE = False
    logger.warning("pyttsx3 not installed. TTS disabled.")


class VoiceInterface:
    """
    Wraps STT and TTS so the agent layer never touches audio libraries directly.
    """

    def __init__(
        self,
        language: str = "en-US",
        tts_rate: int = 170,
        tts_volume: float = 1.0,
        energy_threshold: int = 300,
        pause_threshold: float = 0.8,
    ):
        self.language         = language
        self._tts_rate        = tts_rate
        self._tts_volume      = tts_volume
        self._energy_thresh   = energy_threshold
        self._pause_thresh    = pause_threshold

        self._recognizer  = self._init_recognizer()
        self._tts_engine  = self._init_tts()

    # ------------------------------------------------------------------ #
    #  Public API                                                          #
    # ------------------------------------------------------------------ #

    def listen(self, timeout: int = 5, phrase_limit: int = 15) -> str | None:
        """
        Record from the default microphone and return transcribed text.
        Returns None on silence, timeout, or any error.
        """
        if not _SR_AVAILABLE or self._recognizer is None:
            print("[Voice] STT unavailable — type your message instead.")
            return None

        print("[Listening… speak now]")
        try:
            with sr.Microphone() as source:
                self._recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self._recognizer.listen(
                    source,
                    timeout=timeout,
                    phrase_time_limit=phrase_limit,
                )
            text = self._recognizer.recognize_google(audio, language=self.language)
            return text.strip()
        except sr.WaitTimeoutError:
            logger.debug("Microphone timeout — no speech detected.")
            return None
        except sr.UnknownValueError:
            logger.debug("Speech not understood.")
            return None
        except sr.RequestError as exc:
            logger.error("Google STT request failed: %s", exc)
            return None
        except OSError as exc:
            logger.error("Microphone error: %s", exc)
            return None

    def speak(self, text: str):
        """
        Convert text to speech and play it.
        Falls back to printing if TTS is unavailable.
        """
        clean = text.strip()
        if not clean:
            return

        if self._tts_engine and _PYTTSX3_AVAILABLE:
            try:
                self._tts_engine.say(clean)
                self._tts_engine.runAndWait()
                return
            except Exception as exc:
                logger.error("TTS error: %s", exc)

        # Fallback: print to console
        print(f"[TTS] {clean}")

    # ------------------------------------------------------------------ #
    #  Internal initialisation                                             #
    # ------------------------------------------------------------------ #

    def _init_recognizer(self):
        if not _SR_AVAILABLE:
            return None
        rec = sr.Recognizer()
        rec.energy_threshold = self._energy_thresh
        rec.pause_threshold  = self._pause_thresh
        rec.dynamic_energy_threshold = True
        return rec

    def _init_tts(self):
        if not _PYTTSX3_AVAILABLE:
            return None
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate",   self._tts_rate)
            engine.setProperty("volume", self._tts_volume)
            # Prefer a female English voice if available
            voices = engine.getProperty("voices")
            for v in voices:
                if "female" in v.name.lower() or "zira" in v.name.lower() or "samantha" in v.name.lower():
                    engine.setProperty("voice", v.id)
                    break
            return engine
        except Exception as exc:
            logger.error("pyttsx3 init failed: %s", exc)
            return None
