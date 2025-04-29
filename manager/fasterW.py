from faster_whisper import WhisperModel
import logging
import torch
import json

# function for transcribing audio files using faster-whisper
def transcribe_audio(file_path, model_size="small.en", beam_size=5):
    
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"

    # Load the model
    model = WhisperModel(model_size, device=device, compute_type=compute_type)

    # Transcribe the audio file also using VAD (Voice Activity Detection)
    segments, info = model.transcribe(file_path, beam_size=beam_size, vad_filter=True)
    
    # get the transcription
    full_transcription = dict()
    for segment in segments:
        key = f"{segment.start:.2f}s -> {segment.end:.2f}s"
        full_transcription[key] = segment.text
        



    return full_transcription
