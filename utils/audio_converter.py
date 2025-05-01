# Step 1: Import necessary libraries
from pydub import AudioSegment
import json
from utils import config
import os


# Step 2: Convert MP3 to WAV
def convert_mp3_to_wav(mp3_path, wav_path):
    """Convert MP3 audio file to WAV format."""
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")
    print(f"MP3 file converted to WAV and saved at: {wav_path}")
    return wav_path



# Step 6: Save final output to JSON
def save_results_to_json(results):
    """Save transcription results to a JSON file."""
    os.makedirs('transcripts', exist_ok=True)
    
    transcript_path =f"transcripts/{config.output}.json"
    with open(transcript_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=4, ensure_ascii=False)
    print(f"\n✅ Speaker-attributed transcription saved to: {transcript_path}")