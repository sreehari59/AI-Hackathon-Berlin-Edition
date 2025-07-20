from pydantic import BaseModel
from typing import Optional, List, Literal

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

# Chat models
class ChatMessage(BaseModel):
    role: Literal["user", "assistant", "system"]
    content: str

class ChatRequest(BaseModel):
    messages: List[ChatMessage]

class ChatResponse(BaseModel):
    message: ChatMessage
