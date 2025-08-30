import os
import random
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

from models import SessionCreateResponse, AnalyzeRequest, AnalyzeResponse
from storage import init_db, new_session, touch_session, add_interaction, get_history
from auth_youtube import search_track_by_emotion
from mood_simple import analyze_emotion  # Using simple mood for development
from custom_playlists import get_playlist_info, add_playlist_to_emotion, remove_playlist_from_emotion
import requests

load_dotenv()
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "http://localhost:5173")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    init_db()
    yield
    # Shutdown (if needed)

app = FastAPI(title="TextMood DJ API", lifespan=lifespan)

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


@app.get("/")
def health():
    return {"status": "ok", "service": "textmood-dj backend"}

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
def analyze(req: AnalyzeRequest, request: Request, response: Response):
    sid = get_or_create_session(request, response)
    text = (req.text or "").strip()
    if not text:
        return JSONResponse(status_code=400, content={"detail": "text is required"})

    emotion, conf = analyze_emotion(text)
    track = search_track_by_emotion(emotion)

    # GIPHY
    meme_url = None
    try:
        g = requests.get(
            "https://api.giphy.com/v1/gifs/search",
            params={"api_key": GIPHY_API_KEY, "q": emotion, "limit": 25, "rating": "pg"},
            timeout=10
        )
        g.raise_for_status()
        data = g.json().get("data", [])
        if data:
            # Randomly select a meme from the results
            random_meme = random.choice(data)
            meme_url = random_meme["images"]["original"]["url"]
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

# Playlist management endpoints
@app.get("/api/playlists")
def get_playlists():
    """Get all configured playlists for each emotion"""
    return get_playlist_info()

@app.post("/api/playlists/{emotion}/add")
def add_playlist(emotion: str, playlist_data: dict):
    """Add a playlist URL to a specific emotion"""
    playlist_url = playlist_data.get("playlist_url")
    if not playlist_url:
        return JSONResponse(
            status_code=400,
            content={"detail": "playlist_url is required"}
        )
    
    success = add_playlist_to_emotion(emotion, playlist_url)
    if success:
        return {"message": f"Playlist added to {emotion} emotion successfully"}
    else:
        return JSONResponse(
            status_code=400,
            content={"detail": "Failed to add playlist. Check if URL is valid or already exists."}
        )

@app.delete("/api/playlists/{emotion}/remove")
def remove_playlist(emotion: str, playlist_data: dict):
    """Remove a playlist URL from a specific emotion"""
    playlist_url = playlist_data.get("playlist_url")
    if not playlist_url:
        return JSONResponse(
            status_code=400,
            content={"detail": "playlist_url is required"}
        )
    
    success = remove_playlist_from_emotion(emotion, playlist_url)
    if success:
        return {"message": f"Playlist removed from {emotion} emotion successfully"}
    else:
        return JSONResponse(
            status_code=400,
            content={"detail": "Playlist not found in the specified emotion."}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
