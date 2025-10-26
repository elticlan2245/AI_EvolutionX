from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional
import io
from ..services.voice_service import voice_service

router = APIRouter(prefix="/api/voice", tags=["voice"])

class TTSRequest(BaseModel):
    text: str
    language: str = "es"
    slow: bool = False

@router.post("/synthesize")
async def synthesize_speech(request: TTSRequest):
    """Convert text to speech"""
    try:
        audio_data = await voice_service.text_to_speech(
            text=request.text,
            language=request.language,
            slow=request.slow
        )
        
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "inline; filename=speech.mp3"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcribe")
async def transcribe_audio(audio: UploadFile = File(...)):
    """Transcribe audio to text (placeholder for future implementation)"""
    try:
        # TODO: Implement with Whisper or similar
        return {
            "text": "Audio transcription coming soon",
            "language": "es",
            "confidence": 0.0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
