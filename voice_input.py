import whisper
import sounddevice as sd
import numpy as np
import scipy.io.wavfile as wavfile

duration = 5
samplerate = 44100
filename = "input.wav"

def record_and_transcribe():
    print("🎙️ Listening...")
    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()
    wavfile.write(filename, samplerate, recording)

    model = whisper.load_model("small", device="cuda")  # Use device='cuda' for GPU

    result = model.transcribe(filename)
    print("📝 You said:", result["text"])
    return result["text"]
