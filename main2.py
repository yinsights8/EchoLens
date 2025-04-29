import asyncio
import os
import logging
from uuid import uuid4

from manager.audio import record_audio  # your audio.py file
from manager.fasterW import transcribe_audio  # your transcribe.py file

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def record_and_enqueue(queue: asyncio.Queue, output_dir="audio"):
    os.makedirs(output_dir, exist_ok=True)
    index = 0
    while True:
        filename = f"{uuid4().hex[:6]}_{index}.mp3"
        audio_path = os.path.join(output_dir, filename)

        # Run blocking record_audio in a thread
        await asyncio.to_thread(record_audio, audio_path)
        logging.info(f"✅ Audio saved: {audio_path}")

        await queue.put(audio_path)
        index += 1
        await asyncio.sleep(0.5)

async def transcribe_from_queue(queue: asyncio.Queue):
    while True:
        audio_path = await queue.get()
        try:
            logging.info(f"🔍 Transcribing {audio_path}")
            await asyncio.to_thread(transcribe_audio, audio_path)
        except Exception as e:
            logging.error(f"❌ Error transcribing {audio_path}: {e}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    await asyncio.gather(
        record_and_enqueue(queue),
        transcribe_from_queue(queue),
    )

if __name__ == "__main__":
    asyncio.run(main())