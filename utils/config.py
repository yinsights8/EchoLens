import os
import time


os.makedirs("audio", exist_ok=True)
output = time.strftime("%Y-%m-%d_%H-%M-%S")
AUDIO_FILE_PATH = f"audio/{output}.mp3"