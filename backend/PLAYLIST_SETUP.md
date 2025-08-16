# Example: How to Add Your Custom Playlists

This system allows you to add YouTube playlist URLs for each emotion. When someone types "I'm happy", the system will randomly pick a song from one of your happy playlists.

## How to Add Playlists

### Option 1: Edit the `custom_playlists.py` file directly

Open `backend/custom_playlists.py` and add your playlist URLs:

```python
EMOTION_PLAYLISTS = {
    "happy": [
        "https://www.youtube.com/playlist?list=PLrAl6rYGSt4C8V0E8_ODsVXQw2BzfgOxI",  # Your happy playlist
        "https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # Another happy playlist
    ],
    "sad": [
        "https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # Your sad playlist
    ],
    "angry": [
        "https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # Your rock/metal playlist
    ],
    "calm": [
        "https://www.youtube.com/playlist?list=PLxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # Your chill playlist
    ],
    # Add more emotions as needed
}
```

### Option 2: Use the API endpoints (when backend is running)

```bash
# Add a playlist to the "happy" emotion
curl -X POST "http://localhost:8000/api/playlists/happy/add" \
  -H "Content-Type: application/json" \
  -d '{"playlist_url": "https://www.youtube.com/playlist?list=PLrAl6rYGSt4C8V0E8_ODsVXQw2BzfgOxI"}'

# View all playlists
curl "http://localhost:8000/api/playlists"

# Remove a playlist
curl -X DELETE "http://localhost:8000/api/playlists/happy/remove" \
  -H "Content-Type: application/json" \
  -d '{"playlist_url": "https://www.youtube.com/playlist?list=PLrAl6rYGSt4C8V0E8_ODsVXQw2BzfgOxI"}'
```

## How to Find Playlist URLs

1. Go to YouTube
2. Find or create a playlist
3. Copy the playlist URL (it should look like: `https://www.youtube.com/playlist?list=PLxxxxxxxxx`)
4. Add it to the appropriate emotion category

## How It Works

1. User types "I'm happy"
2. System detects emotion: "happy"
3. System picks a random playlist from the "happy" emotion playlists
4. System picks a random song from that playlist
5. Returns the song to the user

## Fallback System

- If no custom playlists are configured for an emotion, it falls back to YouTube search
- If YouTube API is not available, it uses hardcoded fallback songs
- This ensures the system always works, even without configuration

## Example Workflow

```
Input: "I'm feeling great today!"
↓
Emotion: "happy" (detected)
↓
Random playlist from happy playlists
↓
Random song from that playlist
↓
Output: "Uptown Funk - Mark Ronson ft. Bruno Mars"
```
