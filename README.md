# Empathy Engine 🎤

AI system that converts text into emotionally expressive speech.

## Features
- Emotion detection (Positive, Negative, Neutral)
- Voice modulation (rate control)
- Audio generation

## Tech Stack
- Python
- Flask
- TextBlob
- pyttsx3

## Run Project
pip install -r requirements.txt  
python app.py

## API
POST /generate  
Body: { "text": "Hello world" }