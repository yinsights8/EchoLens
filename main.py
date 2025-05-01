from utils import config
from manager.recorder import start_spacebar_recording
from utils.audio_converter import convert_mp3_to_wav, save_results_to_json
from manager.diarization import speaker_diarization
from manager.fasterW import initialize_whisper_model, process_segments
from pydub import AudioSegment
import os

import warnings
warnings.filterwarnings("ignore")

# start recording
start_spacebar_recording()

#convert the audio file to wav format
wav_file = convert_mp3_to_wav(mp3_path=config.AUDIO_MP3_FILE_PATH, wav_path=config.AUDIO_WAV_FILE_PATH)

# diarize the audio file
diarization = speaker_diarization(wav_file=wav_file)

# Initialize Whisper model
whisper = initialize_whisper_model(model_size = config.MODEL_NAME)

# Load full audio for segment processing
full_audio = AudioSegment.from_wav(wav_file)
    
    
# Process segments and transcribe
results = process_segments(diarization, whisper, full_audio)

# save results to JSON file
save_results_to_json(results)      
                                                                                                                                                                         