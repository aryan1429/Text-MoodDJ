import os
from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

from models import SessionCreateResponse, AnalyzeRequest, AnalyzeResponse
from storage import init_db, new_session, touch_session, add_interaction, get_history
from auth_youtube import search_track_by_emotion
from mood_simple import analyze_emotion
from custom_playlists import get_playlist_info, add_playlist_to_emotion, remove_playlist_from_emotion
import requests

load_dotenv()
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "http://localhost:5173")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

app = FastAPI(title="TextMood DJ API")

# Configure CORS properly for credentials
allowed_origins = [
    "http://localhost:5173",  # Vite dev server default
    "http://127.0.0.1:5173",  # Alternative localhost
    "http://localhost:5174",  # Vite dev server alternate port
    "http://127.0.0.1:5174",  # Alternative localhost
    ALLOWED_ORIGIN
] if ALLOWED_ORIGIN not in ["*", "http://localhost:5173"] else [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def _startup():
    init_db()

def get_or_create_session(request: Request, response: Response) -> str:
    # check header or cookie
    sid = request.headers.get("X-Session-Id") or request.cookies.get("session_id")
    if sid:
        touch_session(sid)
        return sid
    sid = new_session()
    response.set_cookie("session_id", sid, httponly=True, secure=False, samesite="lax")
    return sid

@app.get("/api/session", response_model=SessionCreateResponse)
async def create_session(request: Request, response: Response):
    sid = get_or_create_session(request, response)
    return SessionCreateResponse(session_id=sid)

@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(request: Request, response: Response, req: AnalyzeRequest):
    sid = get_or_create_session(request, response)
    emotion, conf = analyze_emotion(req.text)
    track = search_track_by_emotion(emotion)

    # GIPHY
    meme_url = None
    try:
        g = requests.get(
            "https://api.giphy.com/v1/gifs/search",
            params={"api_key": GIPHY_API_KEY, "q": emotion, "limit": 10, "rating": "pg"},
            timeout=10
        )
        g.raise_for_status()
        data = g.json().get("data", [])
        if data:
            meme_url = data[0]["images"]["original"]["url"]
    except Exception as e:
        print(f"GIPHY error: {e}")
        meme_url = None

    add_interaction(sid, req.text, emotion)
    return AnalyzeResponse(
        session_id=sid,
        emotion=emotion,
        confidence=conf,
        track=track,
        meme_url=meme_url,
        quote=None
    )

@app.get("/api/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8002)

