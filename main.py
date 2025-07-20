import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv
from orchestrator_agent import orchestrate_trip

from models import VoiceInputRequest, TripRequest, TripPlanResponse, ChatRequest, ChatResponse
from openai_client import transcribe_audio, get_trip_plan, chat_completion

load_dotenv()  # Load your .env file

app = FastAPI(
    title="AI Chatbot Interface",
    description="A chatbot interface similar to ChatGPT or Perplexity"
)

# For easy local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a static directory if it doesn't exist
os.makedirs("static", exist_ok=True)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/api/voice/process")
async def process_voice(input: VoiceInputRequest):
    if not input.audio_base64 and not input.text:
        raise HTTPException(status_code=400, detail="No audio or text supplied.")
    if input.text:
        text = input.text
    else:
        # Call Whisper model or placeholder
        text = await transcribe_audio(input.audio_base64)
    return {"transcript": text}

@app.post("/api/trip/create", response_model=TripPlanResponse)
async def create_trip_plan(request: TripRequest):
    plan_data = await orchestrate_trip(request.conversation)
    return TripPlanResponse(itinerary=plan_data["itinerary"])

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Handle chat conversations with the AI assistant.
    """
    response_message = await chat_completion(request.messages)
    return ChatResponse(message=response_message)

# Run the server when this file is executed directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
