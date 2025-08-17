import os
from fastapi import FastAPI, Request, Response, Depends, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health():
    return {"status": "ok"}

@app.post("/api/analyze-voice")
async def analyze_voice(audio: UploadFile = File(...)):
    try:
        print(f"=== Voice Analysis Request Started ===")
        
        # Read audio data
        audio_data = await audio.read()
        print(f"Received audio file: {audio.filename}, size: {len(audio_data)} bytes, content-type: {audio.content_type}")
        
        # Validate audio data
        if len(audio_data) == 0:
            print("Error: Empty audio data received")
            return JSONResponse(
                status_code=400, 
                content={"detail": "Empty audio data received. Please try recording again."}
            )
        
        return {
            "session_id": "test",
            "emotion": "happy",
            "confidence": 0.8,
            "track": None,
            "meme_url": None,
            "transcribed_text": "test transcription"
        }
    
    except Exception as e:
        print(f"Error in analyze_voice: {e}")
        import traceback
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error: {str(e)}"}
        )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8003, log_level="debug")
