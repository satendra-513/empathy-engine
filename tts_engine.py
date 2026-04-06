from gtts import gTTS
import os

def speak(text, emotion):
    
    # Emotion → speed mapping
    if emotion == "positive":
        slow = False
    elif emotion == "negative":
        slow = True
    else:
        slow = False

    tts = gTTS(text=text, lang='en', slow=slow)

    file_path = f"outputs/output_{emotion}.mp3"
    tts.save(file_path)

    return file_path