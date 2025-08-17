import random

# Simple mood analysis for development
def analyze_emotion(text: str):
    """
    Enhanced rule-based emotion detection with extensive keyword matching.
    Replace with transformers model for production.
    """
    text_lower = text.lower()
    
    # Enhanced keyword-based emotion detection with many more options
    
    # Joy/Happiness - expanded with more variations
    joy_keywords = [
        'happy', 'joy', 'joyful', 'excited', 'great', 'awesome', 'amazing', 'love', 'fantastic',
        'wonderful', 'brilliant', 'excellent', 'superb', 'delighted', 'thrilled', 'ecstatic',
        'elated', 'cheerful', 'upbeat', 'optimistic', 'positive', 'blessed', 'grateful',
        'content', 'satisfied', 'pleased', 'gleeful', 'merry', 'blissful', 'euphoric',
        'overjoyed', 'radiant', 'beaming', 'buoyant', 'jubilant', 'exhilarated', 'triumphant',
        'victorious', 'successful', 'accomplished', 'proud', 'confident', 'energetic',
        'vibrant', 'alive', 'spirited', 'enthusiastic', 'passionate', 'motivated'
    ]
    
    # Sadness - expanded with more variations
    sadness_keywords = [
        'sad', 'depressed', 'down', 'terrible', 'awful', 'upset', 'cry', 'crying',
        'heartbroken', 'miserable', 'gloomy', 'melancholy', 'sorrowful', 'grief',
        'mourning', 'devastated', 'crushed', 'broken', 'hurt', 'pain', 'anguish',
        'despair', 'hopeless', 'helpless', 'lonely', 'isolated', 'empty', 'void',
        'disappointed', 'let down', 'discouraged', 'defeated', 'lost', 'confused',
        'overwhelmed', 'stressed', 'tired', 'exhausted', 'drained', 'weary',
        'blue', 'low', 'dark', 'heavy', 'numb', 'withdrawn', 'tearful'
    ]
    
    # Anger - expanded with more variations
    anger_keywords = [
        'angry', 'mad', 'furious', 'hate', 'annoyed', 'frustrated', 'irritated',
        'enraged', 'livid', 'irate', 'outraged', 'infuriated', 'incensed', 'seething',
        'pissed', 'ticked off', 'fed up', 'sick of', 'disgusted', 'appalled',
        'indignant', 'resentful', 'bitter', 'hostile', 'aggressive', 'violent',
        'explosive', 'raging', 'steaming', 'boiling', 'fuming', 'wrathful',
        'vengeful', 'spiteful', 'vindictive', 'contemptuous', 'scornful', 'disdainful'
    ]
    
    # Fear/Anxiety - expanded with more variations
    fear_keywords = [
        'scared', 'afraid', 'worried', 'anxious', 'fear', 'fearful', 'nervous',
        'terrified', 'petrified', 'horrified', 'panicked', 'paranoid', 'alarmed',
        'startled', 'spooked', 'frightened', 'intimidated', 'threatened', 'vulnerable',
        'insecure', 'uncertain', 'doubtful', 'hesitant', 'apprehensive', 'uneasy',
        'restless', 'agitated', 'jittery', 'tense', 'stressed', 'pressure',
        'overwhelmed', 'claustrophobic', 'phobic', 'dread', 'foreboding', 'ominous',
        'suspicious', 'wary', 'cautious', 'vigilant', 'on edge', 'jumpy'
    ]
    
    # Surprise - expanded with more variations
    surprise_keywords = [
        'surprised', 'shocked', 'amazed', 'wow', 'unexpected', 'astonished',
        'astounded', 'stunned', 'bewildered', 'dumbfounded', 'flabbergasted',
        'speechless', 'blown away', 'mind blown', 'incredible', 'unbelievable',
        'remarkable', 'extraordinary', 'phenomenal', 'spectacular', 'breathtaking',
        'jaw dropping', 'eye opening', 'revelation', 'epiphany', 'realization',
        'discovery', 'breakthrough', 'plot twist', 'sudden', 'abrupt', 'startling'
    ]
    
    # Love/Affection - new category
    love_keywords = [
        'love', 'adore', 'cherish', 'treasure', 'devoted', 'infatuated', 'smitten',
        'romantic', 'passion', 'passionate', 'intimate', 'tender', 'affectionate',
        'caring', 'warm', 'fond', 'attached', 'connected', 'bonded', 'close',
        'special', 'meaningful', 'deep', 'heartfelt', 'sincere', 'genuine',
        'crush', 'attraction', 'chemistry', 'spark', 'relationship', 'partner'
    ]
    
    # Calm/Peace - expanded
    calm_keywords = [
        'calm', 'peaceful', 'relaxed', 'chill', 'serene', 'tranquil', 'zen',
        'centered', 'balanced', 'composed', 'collected', 'steady', 'stable',
        'grounded', 'quiet', 'still', 'gentle', 'soft', 'soothing', 'comforting',
        'restful', 'leisurely', 'unhurried', 'patient', 'mindful', 'meditative',
        'reflective', 'contemplative', 'introspective', 'harmonious', 'unified'
    ]
    
    # Disgust - expanded
    disgust_keywords = [
        'disgusted', 'gross', 'yuck', 'horrible', 'revolting', 'repulsive',
        'nauseating', 'sickening', 'vile', 'foul', 'nasty', 'repugnant',
        'abhorrent', 'loathsome', 'detestable', 'offensive', 'distasteful',
        'unpleasant', 'disagreeable', 'objectionable', 'appalling', 'shocking',
        'disturbing', 'unsettling', 'uncomfortable', 'awkward', 'cringe', 'ick'
    ]
    
    # Excitement/Energy - new category
    excitement_keywords = [
        'excited', 'thrilled', 'pumped', 'hyped', 'energetic', 'enthusiastic',
        'eager', 'keen', 'fired up', 'charged', 'electric', 'dynamic', 'lively',
        'spirited', 'animated', 'vivacious', 'exuberant', 'zestful', 'vigorous',
        'intense', 'passionate', 'fervent', 'zealous', 'ardent', 'avid'
    ]
    
    # Confidence - new category
    confidence_keywords = [
        'confident', 'sure', 'certain', 'determined', 'strong', 'powerful',
        'bold', 'brave', 'courageous', 'fearless', 'assertive', 'self-assured',
        'poised', 'composed', 'secure', 'capable', 'competent', 'skilled',
        'accomplished', 'successful', 'victorious', 'triumphant', 'winning'
    ]
    
    # Gratitude - new category
    gratitude_keywords = [
        'grateful', 'thankful', 'appreciative', 'blessed', 'fortunate', 'lucky',
        'privileged', 'honored', 'humbled', 'touched', 'moved', 'inspired',
        'uplifted', 'encouraged', 'supported', 'valued', 'respected', 'loved'
    ]
    
    # Check for emotions in order of specificity
    if any(word in text_lower for word in love_keywords):
        return 'love', random.uniform(0.8, 0.95)
    elif any(word in text_lower for word in excitement_keywords):
        return 'joy', random.uniform(0.85, 0.95)
    elif any(word in text_lower for word in confidence_keywords):
        return 'joy', random.uniform(0.8, 0.9)
    elif any(word in text_lower for word in gratitude_keywords):
        return 'joy', random.uniform(0.8, 0.9)
    elif any(word in text_lower for word in joy_keywords):
        return 'joy', random.uniform(0.8, 0.95)
    elif any(word in text_lower for word in sadness_keywords):
        return 'sadness', random.uniform(0.7, 0.9)
    elif any(word in text_lower for word in anger_keywords):
        return 'anger', random.uniform(0.75, 0.9)
    elif any(word in text_lower for word in fear_keywords):
        return 'fear', random.uniform(0.7, 0.85)
    elif any(word in text_lower for word in surprise_keywords):
        return 'surprise', random.uniform(0.7, 0.9)
    elif any(word in text_lower for word in calm_keywords):
        return 'joy', random.uniform(0.8, 0.95)  # Map calm to joy as it's positive
    elif any(word in text_lower for word in disgust_keywords):
        return 'disgust', random.uniform(0.7, 0.85)
    else:
        return 'neutral', random.uniform(0.6, 0.8)
