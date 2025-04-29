import torch
from manager.audio import record_audio, play_audio
from faster_whisper import WhisperModel
from utils import config
import pyaudio
import wave
import os

def record_chunk(p, stream, file_path, chunk_length=1):
    frames=[]
    for _ in range(0, int(16000 / 1024 * chunk_length)):
        data = stream.read(1024)
        frames.append(data)
        
    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()
    
    
def transcribe_chunks(file_path, model):
    """
    Transcribe the audio file using the Whisper model.
    
    Args:
    file_path (str): The path to the audio file to transcribe.
    
    Returns:
    str: The transcribed text.
    """
    # Transcribe the audio file using the Whisper model
    segments, info = model.transcribe(file_path, beam_size=5, vad_filter=True)
    return " ".join([segment.text for segment in segments])
    

def main():
    model_size = "small.en"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    compute_type = "float16" if device == "cuda" else "int8"
    
    model = WhisperModel(model_size, device=device, compute_type=compute_type)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    
    acuumulated_transcription = ""
    
    try:
        while True:
            # Record a chunk of audio
            file_path = 'temp.wav'
            record_audio(file_path)
            
            # Transcribe the recorded audio
            transcription  = transcribe_chunks(file_path, model)
            print(transcription)
            os.remove(file_path)
            
            
            # append the transcription to the accumulated transcription
            acuumulated_transcription += transcription + " "
            
    except KeyboardInterrupt:
        print("Recording stopped.")
        # write the accumulated transcription to a file
        with open("transcription.txt", "w") as f:
            f.write(acuumulated_transcription)
    finally:
        print("LOG:" + acuumulated_transcription)
        stream.stop_stream()
        stream.close()
        p.terminate()
        
if __name__ == "__main__":
    main()
            