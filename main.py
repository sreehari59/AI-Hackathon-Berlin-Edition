import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from orchestrator_agent import orchestrate_trip

from models import VoiceInputRequest, TripRequest, TripPlanResponse
from openai_client import transcribe_audio, get_trip_plan

load_dotenv()  # Load your .env file

app = FastAPI(
    title="AI Group Trip Planner (Phase 1 MVP)",
    description="Voice-to-Plan backend for group travel"
)

# For easy local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
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