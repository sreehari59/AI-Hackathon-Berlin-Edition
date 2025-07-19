import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
import httpx
  # Load environment variables from .env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
# Debugging line to check if the key is loaded
# Function to interact with OpenAI Whisper API (example - mock, use actual API as needed)
async def transcribe_audio(audio_base64: str):
    # In real use: post to OpenAI's /audio/transcriptions endpoint.
    # Placeholder: Return mock transcription.
    return "transcribed text from audio"

# Function to interact with OpenAI GPT-4 (intent/plan extraction)
async def get_trip_plan(conversation: str):
    url = "https://api.openai.com/v1/chat/completions"
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful travel planning assistant. Extract itinerary, budget, group info from user requests."},
            {"role": "user", "content": conversation}
        ],
        "max_tokens": 500,
    }
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload, headers=headers, timeout=60)
        resp.raise_for_status()
    answer = resp.json()["choices"][0]["message"]["content"]
    return answer