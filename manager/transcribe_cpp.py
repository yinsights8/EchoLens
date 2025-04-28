import subprocess
import os
import logging

def transcriber(audio_file, model_path="whisper.cpp\models\ggml-medium.bin"):
    whisper_executable = r"whisper.cpp\build\bin\Release\whisper-cli.exe"  # your whisper-cli path
    
    # Check if executable exists
    if not os.path.isfile(whisper_executable):
        print("❌ whisper-cli.exe not found at:", whisper_executable)
        return
    
    # Check if audio file exists
    if not os.path.isfile(audio_file):
        print("❌ Audio file not found:", audio_file)
        return

    # Base name for output txt file
    output_txt_file = audio_file + ".txt"
    
    # Run whisper-cli
    result = subprocess.run(
        [
            whisper_executable,
            "-m", model_path,
            "-f", audio_file,
            "-otxt",      # save transcription as text
            # "-nt"         # timestamps
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Print any errors from whisper-cli
    # if result.stderr:
    #     print("\n⚠️ stderr:", result.stderr)
    
    # Now check if the text file was created
    if os.path.exists(output_txt_file):
        with open(output_txt_file, "r", encoding="utf-8") as f:
            transcription_text = f.read()
            logging.info("\n📜 Transcription:\n", transcription_text)
            return transcription_text
    else:
        print("\n❌ Transcription file still not found! Check stderr above.")
        return None
