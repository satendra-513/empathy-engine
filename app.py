from flask import Flask, request, jsonify, render_template
from emotion import detect_emotion
from tts_engine import speak
import os

# ✅ FIRST create app
app = Flask(__name__)

# ✅ UI Home Page
@app.route('/')
def home():
    return render_template("index.html")

# ✅ UI Form Handler
@app.route('/generate_ui', methods=['POST'])
def generate_ui():
    text = request.form.get("text")
    emotion = detect_emotion(text)
    audio_file = speak(text, emotion)

    return f"Emotion: {emotion} <br><audio controls src='/{audio_file}'></audio>"

# ✅ API Endpoint
@app.route('/generate', methods=['POST'])
def generate_voice():
    data = request.json
    text = data.get("text")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    emotion = detect_emotion(text)
    audio_file = speak(text, emotion)

    return jsonify({
        "text": text,
        "emotion": emotion,
        "audio_file": audio_file
    })

# ✅ Run App
if __name__ == "__main__":
    os.makedirs("outputs", exist_ok=True)
    app.run(debug=True)