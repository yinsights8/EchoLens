from manager.audio import record_audio, play_audio
from manager.transcribe_cpp import transcriber
from utils import config  
# from manager.vad_audio import record_audio_vad, play_vad_audio
import os
import logging

from faster_whisper import WhisperModel
import torch

while True:
    record_audio(config.audio_file)
    # record_audio_vad(file_path=config.output_file)
    

    # transcribe the audio file
    # transcriber(config.output_file)
    transcriber(config.audio_file)