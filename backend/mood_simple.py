import random

# Simple mood analysis for development
def analyze_emotion(text: str):
    """
    Simple rule-based emotion detection for development.
    Replace with transformers model for production.
    """
    text_lower = text.lower()
    
    # Simple keyword-based emotion detection
    if any(word in text_lower for word in ['happy', 'joy', 'excited', 'great', 'awesome', 'amazing', 'love', 'fantastic']):
        return 'happy', random.uniform(0.8, 0.95)
    elif any(word in text_lower for word in ['sad', 'depressed', 'down', 'terrible', 'awful', 'upset', 'cry']):
        return 'sad', random.uniform(0.7, 0.9)
    elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'hate', 'annoyed', 'frustrated']):
        return 'angry', random.uniform(0.75, 0.9)
    elif any(word in text_lower for word in ['scared', 'afraid', 'worried', 'anxious', 'fear', 'nervous']):
        return 'fear', random.uniform(0.7, 0.85)
    elif any(word in text_lower for word in ['surprised', 'shocked', 'amazed', 'wow', 'unexpected']):
        return 'surprise', random.uniform(0.7, 0.9)
    elif any(word in text_lower for word in ['calm', 'peaceful', 'relaxed', 'chill', 'serene']):
        return 'calm', random.uniform(0.8, 0.95)
    elif any(word in text_lower for word in ['disgusted', 'gross', 'yuck', 'horrible', 'revolting']):
        return 'disgust', random.uniform(0.7, 0.85)
    else:
        return 'neutral', random.uniform(0.6, 0.8)
