import pyaudio
from pydub import AudioSegment
from pynput import keyboard
import threading
import logging
from io import BytesIO
import pygame

from utils.config import AUDIO_MP3_FILE_PATH, AUDIO_WAV_FILE_PATH

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants
CHANNELS = 1
RATE = 16000
CHUNK = 1024
MP3_OUTPUT_FILENAME = AUDIO_MP3_FILE_PATH

# Globals
recording = False
frames = []
stream = None
audio_interface = pyaudio.PyAudio()
recording_thread = None


def start_recording():
    global frames, stream, recording
    frames = []

    stream = audio_interface.open(format=pyaudio.paInt16,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK)

    logging.info("Recording started...")
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    logging.info("Recording stopped.")

    # Save directly as MP3 using in-memory WAV
    wav_buffer = BytesIO()
    audio_segment = AudioSegment(
        data=b''.join(frames),
        sample_width=audio_interface.get_sample_size(pyaudio.paInt16),
        frame_rate=RATE,
        channels=CHANNELS
    )
    audio_segment.export(MP3_OUTPUT_FILENAME, format="mp3", bitrate="128k", parameters=["-ar", "22050", "-ac", "1"])
    logging.info(f"Saved MP3 as {MP3_OUTPUT_FILENAME}")


def on_press(key):
    global recording, recording_thread
    if key == keyboard.Key.space and not recording:
        recording = True
        recording_thread = threading.Thread(target=start_recording)
        recording_thread.start()


def on_release(key):
    global recording, recording_thread
    if key == keyboard.Key.space:
        recording = False
        if recording_thread:
            recording_thread.join()
        return False  # Stop the listener


def start_spacebar_recording():
    logging.info("Hold SPACE to record...")
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


def play_audio(file_path):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)
    except Exception as e:
        logging.error(f"Playback error: {e}")
    finally:
        pygame.mixer.quit()


if __name__ == "__main__":
    start_spacebar_recording()
    play_audio(MP3_OUTPUT_FILENAME)
