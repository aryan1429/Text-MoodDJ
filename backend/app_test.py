import os
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

from models import SessionCreateResponse, AnalyzeRequest, AnalyzeResponse
from storage import init_db, new_session, touch_session, add_interaction, get_history
import requests

load_dotenv()
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "*")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

app = FastAPI(title="TextMood DJ API - Test Mode")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN] if ALLOWED_ORIGIN != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

def get_or_create_session(request: Request, response: Response) -> str:
    # check header or cookie
    sid = request.headers.get("X-Session-Id") or request.cookies.get("session_id")
    if sid:
        touch_session(sid)
        return sid
    # create
    ua = request.headers.get("user-agent")
    sid = new_session(ua)
    # set cookie if same-site
    response.set_cookie("session_id", sid, httponly=True, samesite="Lax")
    return sid

@app.get("/api/session", response_model=SessionCreateResponse)
def create_session(request: Request, response: Response):
    sid = get_or_create_session(request, response)
    return SessionCreateResponse(session_id=sid)

@app.post("/api/analyze", response_model=AnalyzeResponse)
def analyze_text(req: AnalyzeRequest, request: Request, response: Response):
    sid = get_or_create_session(request, response)
    text = req.text or ""
    
    # Simple emotion detection for testing
    text_lower = text.lower()
    if any(word in text_lower for word in ['happy', 'joy', 'excited', 'great']):
        emotion, conf = 'joy', 0.85
    elif any(word in text_lower for word in ['sad', 'depressed', 'down']):
        emotion, conf = 'sadness', 0.80
    elif any(word in text_lower for word in ['angry', 'mad', 'furious']):
        emotion, conf = 'anger', 0.75
    else:
        emotion, conf = 'neutral', 0.70

    # Mock track (since we're testing without YouTube API)
    track = {
        "track_name": f"Test Song for {emotion}",
        "artist": "Test Artist",
        "youtube_url": "https://youtube.com/watch?v=test",
        "embed_url": "https://www.youtube.com/embed/test"
    }

    # Get meme
    meme_url = None
    if GIPHY_API_KEY:
        try:
            giphy_url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_API_KEY}&q={emotion}&limit=1&rating=g"
            g = requests.get(giphy_url)
            data = g.json().get("data", [])
            if data:
                meme_url = data[0]["images"]["original"]["url"]
        except Exception:
            meme_url = None

    add_interaction(sid, text, emotion)

    return AnalyzeResponse(
        session_id=sid,
        emotion=emotion,
        confidence=conf,
        track=track,
        meme_url=meme_url,
        quote=None
    )

@app.get("/api/history")
def history(request: Request, response: Response, limit: int = 10):
    sid = get_or_create_session(request, response)
    return {"session_id": sid, "items": get_history(sid, limit=limit)}

@app.get("/")
def root():
    return {"message": "TextMood DJ API - Test Mode", "status": "running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
