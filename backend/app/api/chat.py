from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
import json

from app.core.ollama import ollama
from app.database import get_db
from app.auth import get_current_user

router = APIRouter(prefix="/api/chat", tags=["chat"])
logger = logging.getLogger(__name__)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: Optional[float] = 0.7
    stream: Optional[bool] = True

@router.post("/")
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Chat endpoint with streaming support
    """
    try:
        logger.info(f"💬 Chat request from {current_user.get('email')} using {request.model}")
        
        # Convert messages to ollama format
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        if request.stream:
            # Streaming response
            async def generate():
                try:
                    async for chunk in ollama.chat_stream(
                        model=request.model,
                        messages=messages,
                        temperature=request.temperature
                    ):
                        if chunk:
                            yield f"data: {json.dumps({'content': chunk})}\n\n"
                    
                    yield "data: [DONE]\n\n"
                    
                except Exception as e:
                    logger.error(f"❌ Error in stream: {e}")
                    yield f"data: {json.dumps({'error': str(e)})}\n\n"
            
            return StreamingResponse(
                generate(),
                media_type="text/event-stream"
            )
        else:
            # Non-streaming response
            response = await ollama.chat(
                model=request.model,
                messages=messages,
                temperature=request.temperature
            )
            
            return {
                "message": {
                    "role": "assistant",
                    "content": response.get("message", {}).get("content", "")
                }
            }
            
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send")
async def send_message(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Alternative endpoint for sending messages
    """
    return await chat(request, current_user)
