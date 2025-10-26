from datetime import datetime
from loguru import logger

from app.db.mongodb import mongodb

async def capture_conversation(
    conversation_id: str,
    user_message: str,
    assistant_message: str,
    quality_score: float
):
    """Capture conversation for training"""
    try:
        training_data = {
            "conversation_id": conversation_id,
            "user_message": user_message,
            "assistant_message": assistant_message,
            "quality_score": quality_score,
            "used_in_training": False,
            "created_at": datetime.utcnow()
        }
        
        await mongodb.db.training_data.insert_one(training_data)
        logger.info(f"✅ Conversation captured (score: {quality_score:.2f})")
        
    except Exception as e:
        logger.error(f"Error capturing conversation: {str(e)}")
