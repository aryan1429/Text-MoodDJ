import random
import requests
import os
from typing import Dict, List, Optional

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

# Custom playlists for each emotion
# Add your YouTube playlist URLs here - the system will randomly pick songs from these playlists
EMOTION_PLAYLISTS = {
    "happy": [
        # Add your happy playlist URLs here
        # Example: "https://www.youtube.com/playlist?list=PLrAl6rYGSt4C8V0E8_ODsVXQw2BzfgOxI"
    ],
    "sad": [
        # Add your sad playlist URLs here
    ],
    "angry": [
        # Add your angry/rock playlist URLs here
    ],
    "calm": [
        # Add your calm/chill playlist URLs here
    ],
    "love": [
        # Add your romantic playlist URLs here
    ],
    "excited": [
        # Add your party/energetic playlist URLs here
    ],
    "fear": [
        # Add your dark/ambient playlist URLs here
    ],
    "neutral": [
        # Add your neutral/background playlist URLs here
    ]
}

def extract_playlist_id(playlist_url: str) -> Optional[str]:
    """Extract playlist ID from YouTube playlist URL"""
    if "list=" in playlist_url:
        return playlist_url.split("list=")[1].split("&")[0]
    return None

def get_random_track_from_playlists(emotion: str) -> Optional[Dict]:
    """
    Get a random track from one of the playlists for the given emotion
    """
    emotion_lower = emotion.lower()
    
    # Check if we have playlists for this emotion
    if emotion_lower not in EMOTION_PLAYLISTS or not EMOTION_PLAYLISTS[emotion_lower]:
        print(f"No custom playlists found for emotion: {emotion}")
        return None
    
    # Check if YouTube API key is available
    if not YOUTUBE_API_KEY:
        print("YouTube API key not available, cannot fetch from playlists")
        return get_fallback_track(emotion)
    
    # Try each playlist until we find one that works
    playlists = EMOTION_PLAYLISTS[emotion_lower].copy()
    random.shuffle(playlists)  # Randomize playlist order
    
    for playlist_url in playlists:
        playlist_id = extract_playlist_id(playlist_url)
        if not playlist_id:
            continue
            
        try:
            # Get playlist items from YouTube API
            url = "https://www.googleapis.com/youtube/v3/playlistItems"
            params = {
                "part": "snippet",
                "playlistId": playlist_id,
                "maxResults": 50,  # Get up to 50 videos from playlist
                "key": YOUTUBE_API_KEY
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            items = data.get("items", [])
            
            if not items:
                continue
            
            # Filter out deleted/private videos
            valid_items = [item for item in items if item["snippet"]["title"] != "Deleted video"]
            
            if not valid_items:
                continue
            
            # Pick a random video from the playlist
            selected_item = random.choice(valid_items)
            video_snippet = selected_item["snippet"]
            video_id = video_snippet["resourceId"]["videoId"]
            
            # Get video thumbnail (best quality available)
            thumbnail = None
            thumbnails = video_snippet.get("thumbnails", {})
            for quality in ["maxres", "standard", "high", "medium", "default"]:
                if quality in thumbnails:
                    thumbnail = thumbnails[quality]["url"]
                    break
            
            print(f"Selected random track from playlist for emotion: {emotion}")
            return {
                "track_name": video_snippet["title"],
                "artist": video_snippet["channelTitle"],
                "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
                "youtube_music_url": f"https://music.youtube.com/watch?v={video_id}",
                "embed_url": f"https://www.youtube.com/embed/{video_id}",
                "thumbnail": thumbnail,
                "description": video_snippet.get("description", "")[:200] + "..." if len(video_snippet.get("description", "")) > 200 else video_snippet.get("description", ""),
                "published_at": video_snippet.get("publishedAt", ""),
                "video_id": video_id,
                "playlist_url": playlist_url
            }
            
        except Exception as e:
            print(f"Error fetching from playlist {playlist_url}: {e}")
            continue
    
    # If all playlists failed, return fallback
    print(f"All playlists failed for emotion: {emotion}, using fallback")
    return get_fallback_track(emotion)

def get_fallback_track(emotion: str) -> Dict:
    """Fallback track when playlists are not available"""
    fallback_tracks = {
        "happy": {
            "track_name": "Happy - Pharrell Williams",
            "artist": "Pharrell Williams",
            "youtube_url": "https://www.youtube.com/results?search_query=happy+pharrell+williams",
            "youtube_music_url": "https://music.youtube.com/search?q=happy+pharrell+williams",
            "thumbnail": "https://img.youtube.com/vi/ZbZSe6N_BXs/maxresdefault.jpg",
            "description": "Feel-good music to boost your mood"
        },
        "sad": {
            "track_name": "Mad World - Gary Jules",
            "artist": "Gary Jules",
            "youtube_url": "https://www.youtube.com/results?search_query=mad+world+gary+jules",
            "youtube_music_url": "https://music.youtube.com/search?q=mad+world+gary+jules",
            "thumbnail": "https://img.youtube.com/vi/4N3N1MlvVc4/maxresdefault.jpg",
            "description": "Contemplative music for reflection"
        },
        "angry": {
            "track_name": "Break Stuff - Limp Bizkit",
            "artist": "Limp Bizkit",
            "youtube_url": "https://www.youtube.com/results?search_query=break+stuff+limp+bizkit",
            "youtube_music_url": "https://music.youtube.com/search?q=break+stuff+limp+bizkit",
            "thumbnail": "https://img.youtube.com/vi/ZpUYjpKg9KY/maxresdefault.jpg",
            "description": "High-energy music to channel frustration"
        },
        "calm": {
            "track_name": "Weightless - Marconi Union",
            "artist": "Marconi Union",
            "youtube_url": "https://www.youtube.com/results?search_query=weightless+marconi+union",
            "youtube_music_url": "https://music.youtube.com/search?q=weightless+marconi+union",
            "thumbnail": "https://img.youtube.com/vi/UfcAVejslrU/maxresdefault.jpg",
            "description": "Relaxing ambient music"
        },
        "love": {
            "track_name": "Perfect - Ed Sheeran",
            "artist": "Ed Sheeran",
            "youtube_url": "https://www.youtube.com/results?search_query=perfect+ed+sheeran",
            "youtube_music_url": "https://music.youtube.com/search?q=perfect+ed+sheeran",
            "thumbnail": "https://img.youtube.com/vi/2Vv-BfVoq4g/maxresdefault.jpg",
            "description": "Romantic music for special moments"
        },
        "neutral": {
            "track_name": "Lofi Hip Hop",
            "artist": "ChillHop Music",
            "youtube_url": "https://www.youtube.com/results?search_query=lofi+hip+hop",
            "youtube_music_url": "https://music.youtube.com/search?q=lofi+hip+hop",
            "thumbnail": "https://img.youtube.com/vi/jfKfPfyJRdk/maxresdefault.jpg",
            "description": "Chill background music"
        }
    }
    
    return fallback_tracks.get(emotion.lower(), fallback_tracks["neutral"])

def add_playlist_to_emotion(emotion: str, playlist_url: str) -> bool:
    """
    Add a playlist URL to an emotion category
    
    Args:
        emotion: The emotion category
        playlist_url: YouTube playlist URL
        
    Returns:
        bool: True if added successfully
    """
    emotion_lower = emotion.lower()
    
    # Validate playlist URL
    playlist_id = extract_playlist_id(playlist_url)
    if not playlist_id:
        return False
    
    # Initialize emotion list if it doesn't exist
    if emotion_lower not in EMOTION_PLAYLISTS:
        EMOTION_PLAYLISTS[emotion_lower] = []
    
    # Check if playlist already exists
    if playlist_url not in EMOTION_PLAYLISTS[emotion_lower]:
        EMOTION_PLAYLISTS[emotion_lower].append(playlist_url)
        return True
    
    return False

def remove_playlist_from_emotion(emotion: str, playlist_url: str) -> bool:
    """
    Remove a playlist URL from an emotion category
    
    Args:
        emotion: The emotion category
        playlist_url: YouTube playlist URL
        
    Returns:
        bool: True if removed successfully
    """
    emotion_lower = emotion.lower()
    
    if emotion_lower in EMOTION_PLAYLISTS and playlist_url in EMOTION_PLAYLISTS[emotion_lower]:
        EMOTION_PLAYLISTS[emotion_lower].remove(playlist_url)
        return True
    
    return False

def get_playlist_info() -> Dict:
    """Get information about all configured playlists"""
    return {
        emotion: {
            "playlist_count": len(playlists),
            "playlists": playlists
        }
        for emotion, playlists in EMOTION_PLAYLISTS.items()
    }