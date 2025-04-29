from manager.audio import record_audio, play_audio
from manager.fasterW import transcribe_audio
from utils import config
import os
import json


# Initialize a container for all transcriptions
full_transcription = {}

try:
    while True:
        file_path = config.AUDIO_FILE_PATH

        # Record and transcribe audio
        record_audio(file_path)
        transcription = transcribe_audio(file_path)

        # Update the full transcription dictionary
        full_transcription.update(transcription)

        # Optional: Print current segment
        print(transcription)

except KeyboardInterrupt:
    # Save all accumulated transcriptions to JSON
    with open("transcription.json", "w", encoding="utf-8") as f:
        json.dump(full_transcription, f, ensure_ascii=False, indent=4)
    print("\nTranscription saved to 'transcription.json'.")