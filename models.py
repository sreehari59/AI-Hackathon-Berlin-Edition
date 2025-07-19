from pydantic import BaseModel
from typing import Optional

class VoiceInputRequest(BaseModel):
    audio_base64: Optional[str] = None
    text: Optional[str] = None

class TripRequest(BaseModel):
    user_id: str
    conversation: str

class TripPlanResponse(BaseModel):
    itinerary: str
    budget_per_person: Optional[float] = None
    suggestions: Optional[str] = None