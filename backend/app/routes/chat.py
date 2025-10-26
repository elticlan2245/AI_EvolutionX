from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from typing import List, Dict, Optional
from pydantic import BaseModel
import json
from ..services.ollama_service import get_active_server, chat_completion
from ..services.vision_service import vision_service
from ..database import get_db
from ..auth import get_current_user
from datetime import datetime

router = APIRouter(prefix="/api", tags=["chat"])

class ChatRequest(BaseModel):
    model: str
    messages: List[Dict[str, str]]
    stream: bool = False
    capture: bool = True
    temperature: float = 0.7
    max_tokens: int = 2048

@router.post("/chat")
async def chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Send a chat message and get a response"""
    try:
        server = await get_active_server()
        if not server:
            raise HTTPException(status_code=503, detail="No Ollama server available")
        
        # Verificar límites si está autenticado
        if current_user["sub"] != "anonymous":
            user = await db.users.find_one({"email": current_user["sub"]})
            if user:
                monthly_limit = user.get("monthly_limit", 100)
                monthly_messages = user.get("monthly_messages", 0)
                
                if monthly_limit != -1 and monthly_messages >= monthly_limit:
                    raise HTTPException(
                        status_code=429,
                        detail=f"Monthly message limit reached. Current: {monthly_messages}/{monthly_limit}"
                    )
                
                await db.users.update_one(
                    {"_id": user["_id"]},
                    {"$inc": {"monthly_messages": 1}}
                )
        
        print(f"[CHAT] Processing with model: {request.model}")
        
        response = await chat_completion(
            model=request.model,
            messages=request.messages,
            stream=request.stream,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        print(f"[CHAT] Response generated successfully")
        
        # Guardar conversación
        if request.capture and not request.stream and current_user["sub"] != "anonymous":
            conversation_data = {
                "user_id": current_user.get("user_id"),
                "model": request.model,
                "messages": request.messages,
                "response": response["message"]["content"],
                "timestamp": datetime.utcnow(),
                "server": server["name"]
            }
            await db.conversations.insert_one(conversation_data)
        
        return response
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[CHAT ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/with-image")
async def chat_with_image(
    model: str = Form(...),
    message: str = Form(...),
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    db = Depends(get_db)
):
    """Send a chat message with an image attachment"""
    try:
        # Validar formato de imagen
        if not vision_service.is_supported_format(image.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image format. Supported: jpg, png, gif, webp"
            )
        
        # Leer imagen
        image_data = await image.read()
        
        # Analizar imagen
        image_info = await vision_service.analyze_image(image_data, image.filename)
        
        print(f"[CHAT] Processing image: {image.filename} ({image_info['size']})")
        
        # Construir mensaje con contexto de imagen
        enhanced_message = f"{message}\n\n[Image attached: {image.filename}, {image_info['size']['width']}x{image_info['size']['height']}px, {image_info['format']}]"
        
        # Enviar a modelo (modelos con visión como llava procesarán la imagen)
        messages = [{"role": "user", "content": enhanced_message}]
        
        server = await get_active_server()
        if not server:
            raise HTTPException(status_code=503, detail="No Ollama server available")
        
        response = await chat_completion(
            model=model,
            messages=messages,
            stream=False,
            temperature=0.7,
            max_tokens=2048
        )
        
        return {
            **response,
            "image_info": image_info
        }
    
    except HTTPException:
        raise
    except Exception as e:
        print(f"[CHAT IMAGE ERROR] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-image")
async def analyze_image_endpoint(
    image: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Analyze an uploaded image"""
    try:
        if not vision_service.is_supported_format(image.filename):
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported image format"
            )
        
        image_data = await image.read()
        image_info = await vision_service.analyze_image(image_data, image.filename)
        
        return image_info
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
