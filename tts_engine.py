import pyttsx3

engine = pyttsx3.init()

def speak(text, emotion):
    
    # Emotion mapping (MUST be inside function)
    if emotion == "positive":
        rate = 190
    elif emotion == "negative":
        rate = 110
    else:
        rate = 150

    engine.setProperty('rate', rate)
    
    # Voice selection
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)

    file_path = f"outputs/output_{emotion}.mp3"
    
    engine.save_to_file(text, file_path)
    engine.runAndWait()
    
    return file_path