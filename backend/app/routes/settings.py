from fastapi import APIRouter, HTTPException, Depends
from typing import Dict, Any
from ..database import get_db

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/")
async def get_settings(db = Depends(get_db)):
    """Get system settings"""
    try:
        settings = await db.settings.find_one({"_id": "global"})
        if not settings:
            settings = {
                "_id": "global",
                "theme": "dark",
                "language": "es",
                "voice_enabled": True,
                "voice_language": "es-ES",
                "voice_speed": 1.0,
                "auto_save": True,
                "show_timestamps": True,
                "default_model": "llama3.1:8b",
                "temperature": 0.7,
                "max_tokens": 2048,
                "training": {
                    "auto_training": True,
                    "min_samples": 100,
                    "quality_threshold": 0.7
                },
                "notifications": {
                    "training_complete": True,
                    "new_model_available": True,
                    "system_alerts": True
                }
            }
            await db.settings.insert_one(settings)
        
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/")
async def update_settings(settings: Dict[str, Any], db = Depends(get_db)):
    """Update settings"""
    try:
        settings.pop("_id", None)
        result = await db.settings.update_one(
            {"_id": "global"},
            {"$set": settings},
            upsert=True
        )
        return {"message": "Settings updated", "modified": result.modified_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models")
async def get_model_settings(db = Depends(get_db)):
    """Get model settings"""
    try:
        models = await db.model_settings.find().to_list(length=100)
        for model in models:
            model["_id"] = str(model["_id"])
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/export")
async def export_settings(db = Depends(get_db)):
    """Export all settings"""
    try:
        settings = await db.settings.find_one({"_id": "global"})
        return settings
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
