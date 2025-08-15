import os
import requests
from typing import Optional, Dict

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

def search_track_by_emotion(emotion: str) -> Optional[Dict]:
    """
    Search for music videos on YouTube based on emotion
    Returns video info that can be played on YouTube/YouTube Music
    """
    
    # Enhanced mood-to-search mapping for better music results
    mood_terms = {
        "happy": "happy upbeat music feel good songs",
        "sad": "sad emotional music heartbreak songs", 
        "angry": "angry rock metal intense music",
        "fear": "dark ambient scary music",
        "surprise": "surprising uplifting electronic music",
        "neutral": "chill lofi beats relaxing music",
        "calm": "calm peaceful acoustic music meditation",
        "excited": "party hype energetic dance music",
        "disgust": "alternative grunge rock music",
        "joy": "joyful celebration happy music",
        "love": "romantic love songs music",
        "anxious": "calming anxiety relief music"
    }
    
    # Get search query for the emotion
    query = mood_terms.get(emotion.lower(), "chill music")
    
    # Add "music" to ensure we get music videos
    search_query = f"{query} music"
    
    try:
        # YouTube Data API v3 search endpoint
        url = "https://www.googleapis.com/youtube/v3/search"
        params = {
            "part": "snippet",
            "q": search_query,
            "type": "video",
            "videoCategoryId": "10",  # Music category
            "order": "relevance",
            "maxResults": 10,
            "key": YOUTUBE_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        items = data.get("items", [])
        
        if not items:
            return None
            
        # Get the first relevant video
        video = items[0]
        video_id = video["id"]["videoId"]
        snippet = video["snippet"]
        
        # Get video thumbnail (best quality available)
        thumbnail = None
        thumbnails = snippet.get("thumbnails", {})
        for quality in ["maxres", "standard", "high", "medium", "default"]:
            if quality in thumbnails:
                thumbnail = thumbnails[quality]["url"]
                break
        
        return {
            "track_name": snippet["title"],
            "artist": snippet["channelTitle"],
            "youtube_url": f"https://www.youtube.com/watch?v={video_id}",
            "youtube_music_url": f"https://music.youtube.com/watch?v={video_id}",
            "embed_url": f"https://www.youtube.com/embed/{video_id}",
            "thumbnail": thumbnail,
            "description": snippet.get("description", "")[:200] + "..." if len(snippet.get("description", "")) > 200 else snippet.get("description", ""),
            "published_at": snippet.get("publishedAt", ""),
            "video_id": video_id
        }
        
    except Exception as e:
        print(f"YouTube API error: {e}")
        return None

def get_video_details(video_id: str) -> Optional[Dict]:
    """
    Get additional details about a specific video
    """
    try:
        url = "https://www.googleapis.com/youtube/v3/videos"
        params = {
            "part": "snippet,statistics,contentDetails",
            "id": video_id,
            "key": YOUTUBE_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        items = data.get("items", [])
        
        if not items:
            return None
            
        video = items[0]
        snippet = video["snippet"]
        stats = video.get("statistics", {})
        
        return {
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "duration": video.get("contentDetails", {}).get("duration", ""),
            "view_count": stats.get("viewCount", "0"),
            "like_count": stats.get("likeCount", "0"),
            "description": snippet.get("description", "")
        }
        
    except Exception as e:
        print(f"YouTube video details error: {e}")
        return None
