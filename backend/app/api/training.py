from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional
from loguru import logger

from app.db.mongodb import mongodb

router = APIRouter()

class TrainingStatus(BaseModel):
    status: str
    samples_collected: int
    samples_ready: int
    last_training: Optional[datetime]
    next_training: Optional[datetime]
    avg_quality_score: float
    total_trainings: int

@router.get("/status", response_model=TrainingStatus)
async def get_training_status():
    """Get training status"""
    try:
        # Count samples
        total_samples = await mongodb.db.training_data.count_documents({})
        ready_samples = await mongodb.db.training_data.count_documents(
            {"quality_score": {"$gte": 0.7}, "used_in_training": False}
        )
        
        # Get average score
        pipeline = [
            {"$group": {"_id": None, "avg_score": {"$avg": "$quality_score"}}}
        ]
        result = await mongodb.db.training_data.aggregate(pipeline).to_list(1)
        avg_score = result[0]["avg_score"] if result else 0.0
        
        # Get last training
        last_training_doc = await mongodb.db.training_runs.find_one(
            sort=[("created_at", -1)]
        )
        last_training = last_training_doc["created_at"] if last_training_doc else None
        
        # Calculate next training
        next_training = None
        if last_training:
            next_training = last_training + timedelta(hours=12)
        
        # Total trainings
        total_trainings = await mongodb.db.training_runs.count_documents({})
        
        return TrainingStatus(
            status="active" if ready_samples >= 100 else "collecting",
            samples_collected=total_samples,
            samples_ready=ready_samples,
            last_training=last_training,
            next_training=next_training,
            avg_quality_score=round(avg_score, 2),
            total_trainings=total_trainings
        )
        
    except Exception as e:
        logger.error(f"Error getting training status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/trigger")
async def trigger_training():
    """Manually trigger training"""
    try:
        # TODO: Implement training trigger
        return {"status": "training_started", "message": "Training job queued"}
    except Exception as e:
        logger.error(f"Error triggering training: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/history")
async def get_training_history(skip: int = 0, limit: int = 20):
    """Get training history"""
    try:
        history = await mongodb.db.training_runs.find().sort(
            "created_at", -1
        ).skip(skip).limit(limit).to_list(limit)
        
        return {"history": history, "total": await mongodb.db.training_runs.count_documents({})}
        
    except Exception as e:
        logger.error(f"Error getting training history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
