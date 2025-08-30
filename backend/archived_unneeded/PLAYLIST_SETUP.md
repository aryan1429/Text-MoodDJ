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
