from fastapi import APIRouter, HTTPException
from datetime import datetime, timedelta
from loguru import logger

from app.db.mongodb import mongodb

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard_stats():
    """Get dashboard statistics"""
    try:
        now = datetime.utcnow()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Conversations today
        conv_today = await mongodb.db.conversations.count_documents(
            {"created_at": {"$gte": today_start}}
        )
        
        # Total conversations
        total_conv = await mongodb.db.conversations.count_documents({})
        
        # Training samples ready
        ready_samples = await mongodb.db.training_data.count_documents(
            {"quality_score": {"$gte": 0.7}, "used_in_training": False}
        )
        
        # Average quality score
        pipeline = [
            {"$group": {"_id": None, "avg_score": {"$avg": "$quality_score"}}}
        ]
        result = await mongodb.db.training_data.aggregate(pipeline).to_list(1)
        avg_score = result[0]["avg_score"] if result else 0.0
        
        return {
            "conversations_today": conv_today,
            "total_conversations": total_conv,
            "training_samples_ready": ready_samples,
            "avg_quality_score": round(avg_score, 2),
            "updated_at": now
        }
        
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
