from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class SessionCreateResponse(BaseModel):
    session_id: str

class AnalyzeRequest(BaseModel):
    text: Optional[str] = None

class AnalyzeResponse(BaseModel):
    session_id: str
    emotion: str
    confidence: float
    track: Optional[dict] = None
    meme_url: Optional[str] = None
    quote: Optional[str] = None

class Interaction(BaseModel):
    id: int = Field(default=0)
    session_id: str
    text: str
    emotion: str
    created_at: datetime
