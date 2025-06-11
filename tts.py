import pyttsx3
import uuid

def text_to_speech(text):
    engine = pyttsx3.init()

    # Set voice properties here to personalize:
    voices = engine.getProperty('voices')
    # Example: choose female voice (usually index 1, but it varies)
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break

    engine.setProperty('rate', 150)  # Speed (default ~200)
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
    # You can add pitch changes if supported by your system (pyttsx3 doesn't support pitch directly though)

    filename = f"output_{uuid.uuid4()}.wav"
    engine.save_to_file(text, filename)
    engine.runAndWait()
    return filename
