import os, time, base64, requests

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

_token_cache = {"access_token": None, "expires_at": 0}

def _fetch_token():
    auth = base64.b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_CLIENT_SECRET}".encode()).decode()
    headers = {"Authorization": f"Basic {auth}"}
    data = {"grant_type": "client_credentials"}
    r = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data, timeout=10)
    r.raise_for_status()
    body = r.json()
    _token_cache["access_token"] = body["access_token"]
    _token_cache["expires_at"] = int(time.time()) + body["expires_in"] - 30

def spotify_token():
    if not _token_cache["access_token"] or time.time() >= _token_cache["expires_at"]:
        _fetch_token()
    return _token_cache["access_token"]

def search_track_by_emotion(emotion: str):
    mood_terms = {
        "happy": "happy upbeat feel good",
        "sad": "sad melancholy piano",
        "angry": "angry intense rock",
        "fear": "dark ambient",
        "surprise": "surprising electronic",
        "neutral": "chill lofi beats",
        "calm": "calm acoustic",
        "excited": "party hype",
        "disgust": "gritty industrial"
    }
    q = mood_terms.get(emotion, "chill lofi beats")
    token = spotify_token()
    headers = {"Authorization": f"Bearer {token}"}
    params = {"q": q, "type": "track", "market": "US", "limit": 10}
    r = requests.get("https://api.spotify.com/v1/search", headers=headers, params=params, timeout=10)
    r.raise_for_status()
    items = r.json().get("tracks", {}).get("items", [])
    # prefer items with preview_url
    for it in items:
        if it.get("preview_url"):
            return {
                "track_name": it["name"],
                "artist": ", ".join([a["name"] for a in it["artists"]]),
                "preview_url": it["preview_url"],
                "external_url": it["external_urls"]["spotify"],
                "image": (it["album"]["images"][0]["url"] if it["album"]["images"] else None)
            }
    # fallback first
    if items:
        it = items[0]
        return {
            "track_name": it["name"],
            "artist": ", ".join([a["name"] for a in it["artists"]]),
            "preview_url": it.get("preview_url"),
            "external_url": it["external_urls"]["spotify"],
            "image": (it["album"]["images"][0]["url"] if it["album"]["images"] else None)
        }
    return None
