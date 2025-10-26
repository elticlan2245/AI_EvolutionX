from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse
import io
from typing import Optional

from ..auth import get_current_user
from ..services.voice_service import VoiceService

router = APIRouter(prefix="/api/voice", tags=["voice"])
voice_service = VoiceService()

@router.post("/synthesize")
async def synthesize_speech(
    text: str,
    voice: str = "default",
    current_user: dict = Depends(get_current_user)
):
    """
    Sintetizar texto a voz
    """
    try:
        audio_data = await voice_service.text_to_speech(text, voice)
        
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={
                "Content-Disposition": "attachment; filename=speech.mp3"
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    Transcribir audio a texto
    """
    try:
        audio_data = await file.read()
        text = await voice_service.speech_to_text(audio_data)
        
        return {
            "text": text,
            "filename": file.filename
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/voices")
async def list_voices(current_user: dict = Depends(get_current_user)):
    """
    Listar voces disponibles
    """
    return {
        "voices": [
            {"id": "default", "name": "Default Voice", "language": "en-US"},
            {"id": "es", "name": "Spanish Voice", "language": "es-ES"},
            {"id": "fr", "name": "French Voice", "language": "fr-FR"}
        ]
    }
