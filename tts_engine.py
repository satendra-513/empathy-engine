"""
tts_engine.py – Multi-Parameter TTS with Emotion-Driven Modulation
Uses pyttsx3 (offline) for final control over rate, pitch, and volume.
Falls back gracefully if pyttsx3 is unavailable.
"""

import os
import time
import pyttsx3
from gtts import gTTS


# ─── Emotion → Voice Parameter Map ───────────────────────────────────────────
# Each entry defines BASE values; intensity will scale them.
# rate   : words-per-minute  (default ~200)
# pitch  : SAPI5 pitch 0-100 (default 50)  — Linux/macOS: not all engines support
# volume : 0.0 – 1.0

_BASE_PARAMS = {
    "excited":     {"rate": 210, "pitch": 65, "volume": 0.98},
    "positive":    {"rate": 195, "pitch": 58, "volume": 0.90},
    "neutral":     {"rate": 180, "pitch": 50, "volume": 0.85},
    "inquisitive": {"rate": 175, "pitch": 55, "volume": 0.87},
    "surprised":   {"rate": 205, "pitch": 68, "volume": 0.93},
    "concerned":   {"rate": 160, "pitch": 44, "volume": 0.82},
    "negative":    {"rate": 155, "pitch": 40, "volume": 0.78},
    "frustrated":  {"rate": 145, "pitch": 35, "volume": 0.75},
}

def _apply_intensity(base: dict, intensity: float, emotion: str) -> dict:
    """
    Scale parameters away from neutral based on intensity (0.0–1.0).
    Positive emotions push rate/pitch UP; negative push them DOWN.
    """
    scale = intensity  # 0.0 = barely any emotion, 1.0 = maximum
    positive_emotions = {"excited", "positive", "surprised"}
    negative_emotions = {"frustrated", "negative", "concerned"}

    rate   = base["rate"]
    pitch  = base["pitch"]
    volume = base["volume"]

    if emotion in positive_emotions:
        rate   += int(scale * 30)   # up to +30 wpm
        pitch  += int(scale * 15)   # up to +15 pitch units
        volume += scale * 0.05      # up to +5%
    elif emotion in negative_emotions:
        rate   -= int(scale * 25)   # up to -25 wpm
        pitch  -= int(scale * 12)   # up to -12 pitch units
        volume -= scale * 0.05      # up to -5%

    return {
        "rate":   max(100, min(300, rate)),
        "pitch":  max(0,   min(100, pitch)),
        "volume": max(0.5, min(1.0, volume)),
    }

def speak(text: str, emotion_result: dict) -> str:
    """
    Synthesise `text` with vocal parameters derived from `emotion_result`.
    Returns the path to the saved .mp3 file.

    emotion_result should be the dict returned by detect_emotion().
    For backward-compat, also accepts a plain emotion string.
    """
    # Support legacy string input
    if isinstance(emotion_result, str):
        emotion_result = {"emotion": emotion_result, "intensity": 0.5, "compound": 0.0}

    emotion   = emotion_result.get("emotion", "neutral")
    intensity = emotion_result.get("intensity", 0.5)

    base   = _BASE_PARAMS.get(emotion, _BASE_PARAMS["neutral"])
    params = _apply_intensity(base, intensity, emotion)

    os.makedirs("outputs", exist_ok=True)
    timestamp = int(time.time())
    wav_path  = os.path.abspath(f"outputs/output_{emotion}_{timestamp}.wav")

    try:
        engine = pyttsx3.init()
        engine.setProperty("rate",   params["rate"])
        engine.setProperty("volume", params["volume"])

        # Pitch is SAPI5 (Windows) / festival-specific – set if supported
        try:
            engine.setProperty("pitch", params["pitch"])
        except Exception:
            pass  # Not all backends support pitch

        engine.save_to_file(text, wav_path)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        # Fallback to gTTS if pyttsx3 fails (e.g. on Render without espeak)
        print(f"Fallback to gTTS due to pyttsx3 error: {e}")
        
        # gTTS only supports 'slow' parameter. 
        # We'll use 'slow' for negative/concerned/frustrated emotions with high intensity.
        is_slow = emotion in ["negative", "concerned", "frustrated"] and intensity > 0.4
        
        tts = gTTS(text=text, lang='en', slow=is_slow)
        tts.save(wav_path)

    return wav_path

    return wav_path