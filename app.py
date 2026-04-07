"""
app.py – Flask Web API for The Empathy Engine
Supports: Web UI, REST API endpoint, and CLI mode.
"""

import os
import argparse
from flask import Flask, request, jsonify, render_template, send_from_directory

from emotion import detect_emotion
from tts_engine import speak

app = Flask(__name__)
os.makedirs("outputs", exist_ok=True)

# ─── Static / audio serving ───────────────────────────────────────────────────
@app.route("/outputs/<filename>")
def serve_audio(filename):
    return send_from_directory(
        os.path.join(os.path.dirname(__file__), "outputs"), filename
    )

# ─── Web UI ───────────────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate_ui", methods=["POST"])
def generate_ui():
    text = request.form.get("text", "").strip()
    if not text:
        return render_template("index.html", error="Please enter some text.")

    emotion_result = detect_emotion(text)
    audio_path     = speak(text, emotion_result)
    filename       = os.path.basename(audio_path)

    return render_template(
        "index.html",
        text=text,
        emotion_result=emotion_result,
        audio_file=filename,
    )

# ─── REST API ─────────────────────────────────────────────────────────────────
@app.route("/generate", methods=["POST"])
def generate_voice():
    data = request.get_json(force=True, silent=True) or {}
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "No text provided"}), 400

    emotion_result = detect_emotion(text)
    audio_path     = speak(text, emotion_result)
    filename       = os.path.basename(audio_path)

    return jsonify({
        "text":      text,
        "emotion":   emotion_result["emotion"],
        "label":     emotion_result["label"],
        "intensity": emotion_result["intensity"],
        "compound":  emotion_result["compound"],
        "audio_url": f"/outputs/{filename}",
        "audio_file": audio_path,
    })

# ─── Health check ─────────────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "ok", "service": "Empathy Engine"})

# ─── CLI mode ─────────────────────────────────────────────────────────────────
def cli_mode():
    parser = argparse.ArgumentParser(description="Empathy Engine – CLI")
    parser.add_argument("--text", "-t", type=str,
                        help="Text to synthesise")
    args = parser.parse_args()

    text = args.text or input("Enter text: ").strip()
    if not text:
        print("No text provided.")
        return

    print(f"\n📝 Text: {text}")
    emotion_result = detect_emotion(text)
    print(f"🎭 Detected Emotion : {emotion_result['label']}")
    print(f"   Intensity         : {emotion_result['intensity']:.2f}")
    print(f"   Compound Score    : {emotion_result['compound']:.3f}")

    print("\n🔊 Synthesising audio…")
    audio_path = speak(text, emotion_result)
    print(f"✅ Audio saved to: {audio_path}")

# ─── Entry point ──────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import sys
    if "--cli" in sys.argv or "-t" in sys.argv or "--text" in sys.argv:
        sys.argv = [a for a in sys.argv if a != "--cli"]
        cli_mode()
    else:
        app.run(debug=True, port=5000)