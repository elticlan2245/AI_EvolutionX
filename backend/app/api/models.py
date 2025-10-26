from fastapi import APIRouter, HTTPException
from typing import List, Dict
import logging

from app.core.ollama import ollama

router = APIRouter(prefix="/api/models", tags=["models"])
logger = logging.getLogger(__name__)

@router.get("/list")
async def list_models():
    """Get list of available Ollama models"""
    try:
        models = await ollama.list_models()
        
        logger.info(f"📋 Found {len(models)} models")
        
        return {
            "models": models,
            "count": len(models)
        }
        
    except Exception as e:
        logger.error(f"❌ Error listing models: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{model_name}")
async def get_model_info(model_name: str):
    """Get detailed information about a specific model"""
    try:
        info = await ollama.get_model_info(model_name)
        return info
        
    except Exception as e:
        logger.error(f"❌ Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/")
async def models_root():
    """Root endpoint - redirects to list"""
    return await list_models()
