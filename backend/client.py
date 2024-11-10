import asyncio
import websockets
import pyaudio
import threading
import logging
import json
import time
import struct

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
AUDIO_SERVER_URL = 'ws://localhost:8000/ws' # Your websocket URL
# Example: AUDIO_SERVER_URL = "ws://localhost:8080/ws/your_user_id"

async def audio_sender(queue, websocket):
    while True:
        audio_data = await queue.get()
        await websocket.send(audio_data)

def record_audio_to_queue(queue, loop):
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    # print("Recording audio...")

    try:
        while True:
            data = stream.read(CHUNK)
            asyncio.run_coroutine_threadsafe(queue.put(data), loop)
    except Exception as e:
        print(f"Error recording audio: {e}")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        asyncio.run_coroutine_threadsafe(queue.put(None), loop)

async def receive_messages(websocket):
    try:
        while True:
            message = await websocket.recv()
            # message = json.loads(message)
            # if message.get('chatType') == 'transcription' or 'transcription_with_response' or 'ova_response_textual':
                # logging.info(message.get('text', '\n'))
            logging.info(message)
    except websockets.ConnectionClosed:
        print("Connection closed")
    except Exception as e:
        print(f"Error receiving message: {e}")

async def main():
    async with websockets.connect(AUDIO_SERVER_URL) as websocket:
        queue = asyncio.Queue()

        loop = asyncio.get_event_loop()
        audio_thread = threading.Thread(target=record_audio_to_queue, args=(queue, loop))
        audio_thread.start()

        await asyncio.gather(
            audio_sender(queue, websocket),
            receive_messages(websocket),
        )

        audio_thread.join()

if __name__ == "__main__":
    asyncio.run(main())