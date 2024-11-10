from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
api_key = os.getenv('OPENAI_API_KEY')

client = OpenAI()

# audio_file = open("audio.wav", "rb")
# transcription = client.audio.transcriptions.create(
#     model="whisper-1",
#     file=audio_file
# )
# print(transcription.text)
def process_audio_with_whisper(): # Save the audio data to a file 
    
    with open("audio.wav", "rb") as audio_file: 
        transcription = client.audio.transcriptions.create( 
            model="whisper-1", file=audio_file 
            ) 
        print(transcription.text)
        return transcription.text
    
if __name__ == "__main__":
    process_audio_with_whisper()