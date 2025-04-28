import os
import time


os.makedirs("audio", exist_ok=True)
output = time.strftime("%Y-%m-%d_%H-%M-%S")
audio_file = f"audio/{output}.mp3"