import asyncio
import websockets
import pyaudio
import threading
import logging
import json
import time
import struct
import openai
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from openai import OpenAI
from dotenv import load_dotenv
import os
from fastapi.middleware.cors import CORSMiddleware
from speech import record_audio
from fastapi import FastAPI, File, UploadFile,Form
from fastapi.responses import JSONResponse

load_dotenv()
client = OpenAI()
OpenAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Audio configuration
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# Initialize FastAPI
app = FastAPI()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
app.add_middleware( CORSMiddleware, allow_origins=["http://localhost:3000","https://openaichatbot-front.onrender.com"], # Allow requests from this origin 
                   allow_credentials=True, 
                   allow_methods=["*"], 
                   allow_headers=["*"],
                     )
chat_history = []
# OpenAI API key
openai.api_key = OpenAI_API_KEY
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)): 
    try:
        contents = await file.read() 
        with open("audio.wav", "wb") as f: 
            f.write(contents) # Process the audio file with Whisper model 
            text = process_audio_with_whisper("audio.wav") # Generate response with GPT-4.0 
            if ( "generate an image" in text.lower() or "create a realistic image" in text.lower() or "generate a realistic image" in text.lower() or "make an image" in text.lower() or "draw an image" in text.lower() or "produce an image" in text.lower() or "render an image" in text.lower() or "design an image" in text.lower() or "illustrate an image" in text.lower() or "generate a picture" in text.lower() or "create a picture" in text.lower() or "make a picture" in text.lower() or "draw a picture" in text.lower() or "produce a picture" in text.lower() or "render a picture" in text.lower() or "design a picture" in text.lower() or "illustrate a picture" in text.lower() or "generate artwork" in text.lower() or "create artwork" in text.lower() or "make artwork" in text.lower() or "draw artwork" in text.lower() or "produce artwork" in text.lower() or "render artwork" in text.lower() or "design artwork" in text.lower() or "illustrate artwork" in text.lower() ): 
                image_url = generate_image_with_dalle(text) 
                chat_history.append({"type": "image", "content": image_url})
                return JSONResponse(content={"image_url": image_url})
            else:
                response = generate_response_with_gpt4(text) 
                chat_history.append({"type": "text", "content": response})
                return JSONResponse(content={"response": response})
    except Exception as e: 
        logging.error(f"Error processing file: {e}") 
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/text-input")
async def text_input(prompt: str = Form(...)):
    try: # Determine if the user is asking for an image 
        if "generate an image" in prompt.lower() or "generate a realistic image" in prompt.lower():
            image_url = generate_image_with_dalle(prompt) 
            chat_history.append({"type": "image", "content": image_url}) 
            return JSONResponse(content={"image_url": image_url}) 
        else: response = generate_response_with_gpt4(prompt) 
        chat_history.append({"type": "text", "content": response}) 
        return JSONResponse(content={"response": response})
    except Exception as e: 
        logging.error(f"Error processing text input: {e}") 
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/image-url-input")
async def image_input(url: str = Form(...), prompt: str = Form(...)): 
    try: 
        image_url = url
        response = process_image_with_gpt4(image_url, prompt) 
        chat_history.append({"type": "text", "content": response}) 
        return JSONResponse(content={"response": response}) 
    except Exception as e: 
        logging.error(f"Error processing image input: {e}") 
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.get("/chat-history")
async def get_chat_history(): 
    return JSONResponse(content={"chat_history": chat_history})

filepath = "audio.wav"

def process_audio_with_whisper(filepath): # Save the audio data to a file 
    # with open("audio.wav", "wb") as f: 
    #     f.write(audio_data) # Transcribe the audio file using OpenAI's Whisper model 
    try:
            audio_file= open(filepath, "rb")
            transcription = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file,
            
            )
            print(transcription.text)
            return transcription.text
    except Exception as e: 
        logging.error(f"Error transcribing audio: {e}") 
        raise

def generate_response_with_gpt4(text):
    try:
        completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": text
            }
        ]
    )
        print(completion.choices[0].message.content)
        return completion.choices[0].message.content
    except Exception as e:
        logging.error(f"Error generating response: {e}") 
        raise



    # response.choices[0].text.strip()

def generate_image_with_dalle(prompt):
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="hd",
    n=1,
)
    return response.data[0].url

def process_image_with_gpt4(url,text): 
    try: 
        
        completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": url,
                        }
                    },
                ],
            }
        ],
    )
        return completion.choices[0].message.content
    except Exception as e: 
        logging.error(f"Error processing image: {e}") 
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
