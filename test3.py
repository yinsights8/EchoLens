from utils import config
from manager.recorder import start_spacebar_recording
from utils.audio_converter import convert_mp3_to_wav, save_results_to_json
from manager.diarization import speaker_diarization
from manager.fasterW import initialize_whisper_model, process_segments
from pydub import AudioSegment
import os

import warnings
warnings.filterwarnings("ignore")


start_spacebar_recording()

wav_file = convert_mp3_to_wav(mp3_path=config.AUDIO_MP3_FILE_PATH, wav_path=config.AUDIO_WAV_FILE_PATH)

# diarize the audio file
diarization = speaker_diarization(wav_file=wav_file)

# Initialize Whisper model
whisper = initialize_whisper_model()

# Load full audio for segment processing
full_audio = AudioSegment.from_wav(wav_file)
    
    
# Process segments and transcribe
results = process_segments(diarization, whisper, full_audio)

# save results to JSON file
save_results_to_json(results, output_json_path=f"output_{config.output}.json")      
                                                                                                                                                                         