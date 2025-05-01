import os
import time


os.makedirs("audio", exist_ok=True)
output = time.strftime("%Y-%m-%d_%H-%M-%S")

AUDIO_MP3_FILE_PATH = f"audio/{output}.mp3"
AUDIO_WAV_FILE_PATH = f"audio/{output}.wav"

# AUDIO_FILE_PATH = "videoplayback.mp3"