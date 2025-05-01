from faster_whisper import WhisperModel
from .diarization import speaker_diarization
import logging
import torch
import json
from utils.audio_converter import convert_mp3_to_wav
from utils import config
import os

# Step 4: Initialize Whisper model
def initialize_whisper_model():
    """Initialize Whisper model with the appropriate compute type."""
    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Select compute_type based on device capabilities
    if device == "cuda" and torch.cuda.is_available():
        # Check if the GPU supports float16 (for better performance on CUDA)
        if torch.cuda.get_device_capability(0)[0] >= 7.0:  # For Volta and newer GPUs
            compute_type = "float16"
        else:
            compute_type = "int8"  # Use int8 on older CUDA GPUs
    else:
        compute_type = "int8"  # Fallback to int8 on CPU or unsupported GPUs

    # Load the model with selected device and compute_type
    model_size = "small.en"  # Change to "large-v1" for larger models
    whisper = WhisperModel(model_size, device=device, compute_type=compute_type)
    return whisper





# Step 5: Process segments and transcribe
def process_segments(diarization, whisper, full_audio):
    """Process diarization segments and transcribe."""
    results = []
    for i, (turn, _, speaker) in enumerate(diarization.itertracks(yield_label=True)):
        start_ms = int(turn.start * 1000)
        end_ms = int(turn.end * 1000)
        speaker_audio = full_audio[start_ms:end_ms]

        # Save temp segment
        temp_segment_path = config.AUDIO_WAV_FILE_PATH
        speaker_audio.export(temp_segment_path, format="wav")

        # Transcribe
        segments, _ = whisper.transcribe(temp_segment_path, beam_size=5, vad_filter=True)
        transcript = " ".join([seg.text for seg in segments])

        # Append result
        results.append({
            "speaker": speaker,
            "start": round(turn.start, 2),
            "end": round(turn.end, 2),
            "text": transcript
        })

        # Remove temp file
        os.remove(temp_segment_path)

    return results