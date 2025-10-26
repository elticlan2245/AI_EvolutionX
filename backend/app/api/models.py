from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from loguru import logger

from app.core.ollama import ollama

router = APIRouter()

class ModelInfo(BaseModel):
    name: str
    size: Optional[int] = None
    modified_at: Optional[str] = None
    digest: Optional[str] = None

@router.get("/", response_model=Dict[str, Any])
async def list_models():
    """List available models"""
    try:
        models = await ollama.list_models()
        return models
    except Exception as e:
        logger.error(f"Error listing models: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/active-server")
async def get_active_server():
    """Get active Ollama server info"""
    if not ollama.active_server:
        await ollama.find_active_server()
    
    if not ollama.active_server:
        raise HTTPException(status_code=503, detail="No Ollama server available")
    
    return ollama.active_server

@router.get("/{model_name}")
async def get_model_info(model_name: str):
    """Get specific model information"""
    try:
        info = await ollama.show_model(model_name)
        return info
    except Exception as e:
        logger.error(f"Error getting model info: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/pull/{model_name}")
async def pull_model(model_name: str):
    """Pull/download a model"""
    try:
        async for progress in ollama.pull_model(model_name):
            # In a real implementation, this would stream progress
            pass
        return {"status": "success", "model": model_name}
    except Exception as e:
        logger.error(f"Error pulling model: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
