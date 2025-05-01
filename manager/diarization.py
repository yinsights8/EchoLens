import torch
from dotenv import load_dotenv
import os
from pyannote.audio import Pipeline

import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


load_dotenv()
hf_token = os.getenv("HF_TOKEN")
print("Hugging Face Token:", hf_token)

def speaker_diarization(wav_file, hf_token=hf_token):
    
    "Run speaker diarization on a wav file using pyannote.audio"
    
    logging.info("Running speaker diarization...")
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", 
                                        use_auth_token=hf_token)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    pipeline.to(device)
    
    diarization = pipeline(wav_file)
    logging.info("Speaker diarization completed.")
    return diarization