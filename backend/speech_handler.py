import whisper
import speech_recognition as sr
import tempfile
import os
from gtts import gTTS
import io

# Global Whisper model
_WHISPER_MODEL = None

def load_whisper_model():
    """Load Whisper model for speech recognition"""
    global _WHISPER_MODEL
    if _WHISPER_MODEL is None:
        print("Loading Whisper model...")
        _WHISPER_MODEL = whisper.load_model("base")
    return _WHISPER_MODEL

def transcribe_audio_file(audio_file_path: str) -> str:
    """
    Transcribe audio file using Whisper
    Args:
        audio_file_path: Path to audio file
    Returns:
        Transcribed text
    """
    try:
        print(f"Loading Whisper model for transcription...")
        model = load_whisper_model()
        print(f"Transcribing file: {audio_file_path}")
        result = model.transcribe(audio_file_path)
        transcribed_text = result["text"].strip()
        print(f"Whisper transcription successful: '{transcribed_text}'")
        return transcribed_text
    except Exception as e:
        print(f"Whisper transcription error: {e}")
        import traceback
        traceback.print_exc()
        return ""

def transcribe_audio_data(audio_data: bytes, format: str = "webm") -> str:
    """
    Transcribe audio data using Whisper
    Args:
        audio_data: Raw audio bytes
        format: Audio format (webm, wav, mp3, etc.)
    Returns:
        Transcribed text
    """
    try:
        print(f"Starting transcription of {len(audio_data)} bytes in {format} format")
        
        # Validate input
        if len(audio_data) == 0:
            print("Error: Empty audio data")
            return ""
        
        # Save audio data to temporary file
        with tempfile.NamedTemporaryFile(suffix=f".{format}", delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file_path = temp_file.name
        
        print(f"Saved audio to temporary file: {temp_file_path}")
        
        # Transcribe using Whisper
        text = transcribe_audio_file(temp_file_path)
        
        # Clean up temporary file
        try:
            os.unlink(temp_file_path)
            print(f"Cleaned up temporary file: {temp_file_path}")
        except Exception as cleanup_error:
            print(f"Warning: Could not clean up temporary file {temp_file_path}: {cleanup_error}")
        
        return text
    except Exception as e:
        print(f"Audio transcription error: {e}")
        import traceback
        traceback.print_exc()
        return ""

def text_to_speech(text: str, lang: str = "en") -> bytes:
    """
    Convert text to speech using gTTS
    Args:
        text: Text to convert
        lang: Language code (default: en)
    Returns:
        Audio bytes (MP3 format)
    """
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save to bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer.read()
    except Exception as e:
        print(f"Text-to-speech error: {e}")
        return b""

def get_emotion_response_text(emotion: str, confidence: float) -> str:
    """
    Generate voice response text based on detected emotion
    Args:
        emotion: Detected emotion
        confidence: Confidence score
    Returns:
        Response text for TTS
    """
    emotion_responses = {
        "joy": f"I can feel the happiness in your words! With {confidence:.0%} confidence, you're feeling joyful.",
        "sadness": f"I sense some sadness there. I'm {confidence:.0%} confident about this feeling.",
        "anger": f"There's some anger in your message. I'm {confidence:.0%} sure about this emotion.",
        "fear": f"I detect some worry or fear. I'm {confidence:.0%} confident about this.",
        "surprise": f"That sounds surprising! I'm {confidence:.0%} sure you're feeling surprised.",
        "disgust": f"I sense some displeasure there. I'm {confidence:.0%} confident about this.",
        "love": f"There's love and warmth in your words! I'm {confidence:.0%} confident.",
        "neutral": f"You seem pretty calm and neutral. I'm {confidence:.0%} confident about this."
    }
    
    return emotion_responses.get(emotion.lower(), 
                                f"I detected {emotion} with {confidence:.0%} confidence.")
