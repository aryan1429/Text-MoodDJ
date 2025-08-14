import os
from fastapi import FastAPI, Request, Response, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from dotenv import load_dotenv
from typing import Optional

from models import SessionCreateResponse, AnalyzeRequest, AnalyzeResponse
from storage import init_db, new_session, touch_session, add_interaction, get_history
from auth_spotify import search_track_by_emotion
from mood_simple import analyze_emotion  # Using simple mood for development
import requests

load_dotenv()
ALLOWED_ORIGIN = os.getenv("ALLOWED_ORIGIN", "*")
GIPHY_API_KEY = os.getenv("GIPHY_API_KEY")

app = FastAPI(title="TextMood DJ API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ALLOWED_ORIGIN] if ALLOWED_ORIGIN != "*" else ["*"],
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
            params={"api_key": GIPHY_API_KEY, "q": emotion, "limit": 10, "rating": "pg"},
            timeout=10
        )
        g.raise_for_status()
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
