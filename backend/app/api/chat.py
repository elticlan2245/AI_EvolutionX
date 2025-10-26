from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from loguru import logger
import asyncio

from app.core.ollama import ollama
from app.db.mongodb import mongodb
from app.db.redis import redis_client
from app.core.capture import capture_conversation
from app.core.scorer import score_conversation

router = APIRouter()

# ======================================================
# modelos pydantic
# ======================================================

class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    model: str
    messages: List[Message]
    temperature: float = 0.7
    max_tokens: int = 2048
    stream: bool = False
    capture: bool = True


class ChatResponse(BaseModel):
    id: Optional[str] = None
    message: Optional[Message] = None
    model: Optional[str] = None
    created_at: Optional[datetime] = None
    captured: bool = False
    quality_score: Optional[float] = None


# ======================================================
# POST /api/chat — conversación normal con stream
# ======================================================

@router.post("/")
async def chat(request: ChatRequest):
    try:
        messages = [{"role": m.role, "content": m.content} for m in request.messages]

        async def generate_response():
            """flujo de tokens desde ollama"""
            try:
                async for chunk in ollama.chat(
                    model=request.model,
                    messages=messages,
                    stream=True,
                    temperature=request.temperature,
                    max_tokens=request.max_tokens
                ):
                    yield chunk
            except Exception as e:
                logger.error(f"ollama streaming error: {str(e)}")
                yield f"[error: {str(e)}]"

        # enviar respuesta en tiempo real
        return StreamingResponse(generate_response(), media_type="text/plain")

    except Exception as e:
        logger.error(f"chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# ======================================================
# WebSocket /api/chat/stream — modo conversación viva
# ======================================================

@router.websocket("/stream")
async def chat_stream(ws: WebSocket):
    await ws.accept()
    logger.info("conexión websocket establecida")

    try:
        while True:
            data = await ws.receive_json()
            model = data.get("model", "llama3.1:8b")
            messages = data.get("messages", [])
            full_response = ""

            logger.debug(f"stream con modelo {model}")

            try:
                async for chunk in ollama.chat(model=model, messages=messages, stream=True):
                    await ws.send_text(chunk)
                    full_response += chunk
            except Exception as e:
                logger.error(f"error en stream ollama: {e}")
                await ws.send_json({"error": str(e)})
                continue

            await ws.send_json({"done": True, "response": full_response})
            logger.info(f"stream finalizado con modelo {model}")

    except WebSocketDisconnect:
        logger.info("websocket desconectado")
    except Exception as e:
        logger.error(f"error websocket: {str(e)}")
        await ws.close()
