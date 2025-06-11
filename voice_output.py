import asyncio
import edge_tts
import uuid
import os
from pydub import AudioSegment
from playsound import playsound

VOICE = "en-US-JennyNeural"

async def _speak(text, filename):
    communicate = edge_tts.Communicate(text, VOICE)
    await communicate.save(filename)

def speak(text):
    mp3_file = f"output_{uuid.uuid4()}.mp3"
    wav_file = mp3_file.replace(".mp3", ".wav")

    asyncio.run(_speak(text, mp3_file))


    audio = AudioSegment.from_mp3(mp3_file)
    audio.export(wav_file, format="wav")


    playsound(wav_file)


    os.remove(mp3_file)
    os.remove(wav_file)
