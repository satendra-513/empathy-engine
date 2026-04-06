from flask import Flask, request, jsonify, render_template, send_from_directory
from emotion import detect_emotion
from tts_engine import speak
import os

# ✅ Create app FIRST
app = Flask(__name__)

# ✅ Serve audio files
@app.route('/outputs/<filename>')
def serve_audio(filename):
    return send_from_directory('outputs', filename)

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

    # ✅ Extract filename properly
    filename = audio_file.split("/")[-1]

    return f"""
    <h3>Emotion: {emotion}</h3>
    <audio controls>
        <source src="/outputs/{filename}" type="audio/mpeg">
    </audio>
    <br><br>
    <a href="/">⬅ Back</a>
    """

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