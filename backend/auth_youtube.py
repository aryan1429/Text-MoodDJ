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
    
    # Check if API key is available
    if not YOUTUBE_API_KEY:
        print("YouTube API key not configured, using fallback recommendations")
        return get_fallback_music(emotion)
    
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
            print("No YouTube results found, using fallback")
            return get_fallback_music(emotion)
            
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
        print(f"YouTube API error: {e}, using fallback recommendations")
        return get_fallback_music(emotion)

def get_fallback_music(emotion: str) -> Dict:
    """
    Fallback music recommendations when YouTube API is unavailable
    """
    # SVG data URI generator for reliable thumbnail placeholders
    def create_thumbnail_svg(color: str, text: str) -> str:
        svg = f'''data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='320' height='180' viewBox='0 0 320 180'%3E%3Crect width='100%25' height='100%25' fill='%23{color}'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='Arial, sans-serif' font-size='20' font-weight='bold' fill='white'%3E{text}%3C/text%3E%3C/svg%3E'''
        return svg
    
    fallback_tracks = {
        "happy": {
            "track_name": "Happy - Pharrell Williams",
            "artist": "Pharrell Williams",
            "youtube_url": "https://www.youtube.com/results?search_query=happy+pharrell+williams",
            "youtube_music_url": "https://music.youtube.com/search?q=happy+pharrell+williams",
            "thumbnail": create_thumbnail_svg("FFD700", "Happy Music"),
            "description": "Feel-good music to boost your mood"
        },
        "joy": {
            "track_name": "Dancing Queen - ABBA",
            "artist": "ABBA",
            "youtube_url": "https://www.youtube.com/results?search_query=dancing+queen+abba",
            "youtube_music_url": "https://music.youtube.com/search?q=dancing+queen+abba",
            "thumbnail": create_thumbnail_svg("FFD700", "Joyful Music"),
            "description": "Classic feel-good music to celebrate"
        },
        "sad": {
            "track_name": "Mad World - Gary Jules",
            "artist": "Gary Jules",
            "youtube_url": "https://www.youtube.com/results?search_query=mad+world+gary+jules",
            "youtube_music_url": "https://music.youtube.com/search?q=mad+world+gary+jules",
            "thumbnail": create_thumbnail_svg("87CEEB", "Sad Music"),
            "description": "Contemplative music for reflection"
        },
        "anger": {
            "track_name": "Break Stuff - Limp Bizkit",
            "artist": "Limp Bizkit",
            "youtube_url": "https://www.youtube.com/results?search_query=break+stuff+limp+bizkit",
            "youtube_music_url": "https://music.youtube.com/search?q=break+stuff+limp+bizkit",
            "thumbnail": create_thumbnail_svg("FF6B6B", "Angry Music"),
            "description": "High-energy music to channel frustration"
        },
        "angry": {
            "track_name": "Break Stuff - Limp Bizkit",
            "artist": "Limp Bizkit",
            "youtube_url": "https://www.youtube.com/results?search_query=break+stuff+limp+bizkit",
            "youtube_music_url": "https://music.youtube.com/search?q=break+stuff+limp+bizkit",
            "thumbnail": create_thumbnail_svg("FF6B6B", "Angry Music"),
            "description": "High-energy music to channel frustration"
        },
        "fear": {
            "track_name": "Requiem for a Dream - Clint Mansell",
            "artist": "Clint Mansell",
            "youtube_url": "https://www.youtube.com/results?search_query=requiem+for+a+dream+soundtrack",
            "youtube_music_url": "https://music.youtube.com/search?q=requiem+for+a+dream+soundtrack",
            "thumbnail": create_thumbnail_svg("9370DB", "Dark Music"),
            "description": "Atmospheric music for intense emotions"
        },
        "surprise": {
            "track_name": "Uptown Funk - Mark Ronson ft. Bruno Mars",
            "artist": "Mark Ronson ft. Bruno Mars",
            "youtube_url": "https://www.youtube.com/results?search_query=uptown+funk+bruno+mars",
            "youtube_music_url": "https://music.youtube.com/search?q=uptown+funk+bruno+mars",
            "thumbnail": create_thumbnail_svg("FFA500", "Surprise Music"),
            "description": "Unexpected and energetic music"
        },
        "love": {
            "track_name": "Perfect - Ed Sheeran",
            "artist": "Ed Sheeran",
            "youtube_url": "https://www.youtube.com/results?search_query=perfect+ed+sheeran",
            "youtube_music_url": "https://music.youtube.com/search?q=perfect+ed+sheeran",
            "thumbnail": create_thumbnail_svg("FF1493", "Love Music"),
            "description": "Romantic music for special moments"
        },
        "neutral": {
            "track_name": "Weightless - Marconi Union",
            "artist": "Marconi Union",
            "youtube_url": "https://www.youtube.com/results?search_query=weightless+marconi+union",
            "youtube_music_url": "https://music.youtube.com/search?q=weightless+marconi+union",
            "thumbnail": create_thumbnail_svg("808080", "Chill Music"),
            "description": "Relaxing ambient music"
        },
        "disgust": {
            "track_name": "Toxicity - System Of A Down",
            "artist": "System Of A Down",
            "youtube_url": "https://www.youtube.com/results?search_query=toxicity+system+of+a+down",
            "youtube_music_url": "https://music.youtube.com/search?q=toxicity+system+of+a+down",
            "thumbnail": create_thumbnail_svg("9ACD32", "Alternative Music"),
            "description": "Alternative rock for strong emotions"
        }
    }
    
    # Get fallback track for emotion, default to neutral
    return fallback_tracks.get(emotion.lower(), fallback_tracks["neutral"])

def get_video_details(video_id: str) -> Optional[Dict]:
    """
    Get additional details about a specific video
    """
    if not YOUTUBE_API_KEY:
        return None
        
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
