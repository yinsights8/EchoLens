import torch
from pyannote.audio import Pipeline
from pydub import AudioSegment
import os
from dotenv import load_dotenv

load_dotenv()
hf_token = os.getenv("HF_TOKEN")
print("Hugging Face Token:", hf_token)

# --- Convert MP3 to temporary WAV ---
mp3_path = "audio/2025-05-01_16-02-50.mp3"
wav_path = "audio/temp_for_diarization.wav"

# Load and export to WAV
audio = AudioSegment.from_mp3(mp3_path)
audio.export(wav_path, format="wav")



pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token=hf_token)

# send pipeline to GPU (when available)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
pipeline.to(torch.device(device))


# apply pretrained pipeline
diarization = pipeline(wav_path)

# print the result
for turn, _, speaker in diarization.itertracks(yield_label=True):
    print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")