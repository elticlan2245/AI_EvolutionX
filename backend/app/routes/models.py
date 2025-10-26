from fastapi import APIRouter, HTTPException
from ..services.ollama_service import get_active_server, list_models

router = APIRouter(prefix="/api", tags=["models"])

@router.get("/models")
async def get_models():
    """Get available models"""
    try:
        server = await get_active_server()
        if not server:
            raise HTTPException(status_code=503, detail="No Ollama server available")
        
        models = await list_models()
        return {"models": models, "server": server["name"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
