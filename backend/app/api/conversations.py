from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime
from loguru import logger

from app.db.mongodb import mongodb

router = APIRouter()

@router.get("/")
async def list_conversations(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    user_id: Optional[str] = None
):
    """List conversations"""
    try:
        query = {}
        if user_id:
            query["user_id"] = user_id
        
        conversations = await mongodb.db.conversations.find(query).sort(
            "created_at", -1
        ).skip(skip).limit(limit).to_list(limit)
        
        total = await mongodb.db.conversations.count_documents(query)
        
        # Convert ObjectId to string
        for conv in conversations:
            conv["_id"] = str(conv["_id"])
        
        return {
            "conversations": conversations,
            "total": total,
            "skip": skip,
            "limit": limit
        }
        
    except Exception as e:
        logger.error(f"Error listing conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get specific conversation"""
    try:
        from bson import ObjectId
        
        conversation = await mongodb.db.conversations.find_one(
            {"_id": ObjectId(conversation_id)}
        )
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conversation["_id"] = str(conversation["_id"])
        return conversation
        
    except Exception as e:
        logger.error(f"Error getting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete conversation"""
    try:
        from bson import ObjectId
        
        result = await mongodb.db.conversations.delete_one(
            {"_id": ObjectId(conversation_id)}
        )
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {"status": "deleted", "id": conversation_id}
        
    except Exception as e:
        logger.error(f"Error deleting conversation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
