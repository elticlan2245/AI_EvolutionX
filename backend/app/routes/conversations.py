from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from bson import ObjectId
from ..database import get_db
from ..models.conversation import Conversation, Message

router = APIRouter(prefix="/api/conversations", tags=["conversations"])

@router.get("/")
async def get_conversations(
    limit: int = Query(50, le=100),
    skip: int = Query(0, ge=0),
    search: Optional[str] = None,
    starred: Optional[bool] = None,
    db = Depends(get_db)
):
    """Get all conversations with filtering"""
    try:
        query = {}
        if search:
            query["$or"] = [
                {"title": {"$regex": search, "$options": "i"}},
                {"messages.content": {"$regex": search, "$options": "i"}}
            ]
        if starred is not None:
            query["starred"] = starred
        
        conversations = await db.conversations.find(query)\
            .sort("updated_at", -1)\
            .skip(skip)\
            .limit(limit)\
            .to_list(length=limit)
        
        total = await db.conversations.count_documents(query)
        
        for conv in conversations:
            conv["_id"] = str(conv["_id"])
            if "messages" in conv:
                conv["message_count"] = len(conv["messages"])
                if conv["messages"]:
                    conv["last_message"] = conv["messages"][-1]["content"][:100]
        
        return {
            "conversations": conversations,
            "total": total,
            "page": skip // limit + 1,
            "pages": (total + limit - 1) // limit
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: str,
    db = Depends(get_db)
):
    """Get a specific conversation with all messages"""
    try:
        if not ObjectId.is_valid(conversation_id):
            raise HTTPException(status_code=400, detail="Invalid conversation ID")
        
        conversation = await db.conversations.find_one({"_id": ObjectId(conversation_id)})
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conversation["_id"] = str(conversation["_id"])
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_conversation(
    title: str = "New Conversation",
    model: str = "llama3.1:8b",
    db = Depends(get_db)
):
    """Create a new conversation"""
    try:
        conversation = {
            "title": title,
            "messages": [],
            "model": model,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "tags": [],
            "starred": False
        }
        
        result = await db.conversations.insert_one(conversation)
        conversation["_id"] = str(result.inserted_id)
        
        return conversation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{conversation_id}/messages")
async def add_message(
    conversation_id: str,
    role: str,
    content: str,
    model: Optional[str] = None,
    tokens: Optional[int] = None,
    db = Depends(get_db)
):
    """Add a message to a conversation"""
    try:
        if not ObjectId.is_valid(conversation_id):
            raise HTTPException(status_code=400, detail="Invalid conversation ID")
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.utcnow(),
            "model": model,
            "tokens": tokens
        }
        
        result = await db.conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {
                "$push": {"messages": message},
                "$set": {"updated_at": datetime.utcnow()}
            }
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {"message": "Message added", "data": message}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{conversation_id}")
async def update_conversation(
    conversation_id: str,
    title: Optional[str] = None,
    starred: Optional[bool] = None,
    tags: Optional[List[str]] = None,
    db = Depends(get_db)
):
    """Update conversation metadata"""
    try:
        if not ObjectId.is_valid(conversation_id):
            raise HTTPException(status_code=400, detail="Invalid conversation ID")
        
        update_data = {"updated_at": datetime.utcnow()}
        
        if title is not None:
            update_data["title"] = title
        if starred is not None:
            update_data["starred"] = starred
        if tags is not None:
            update_data["tags"] = tags
        
        result = await db.conversations.update_one(
            {"_id": ObjectId(conversation_id)},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {"message": "Conversation updated"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: str,
    db = Depends(get_db)
):
    """Delete a conversation"""
    try:
        if not ObjectId.is_valid(conversation_id):
            raise HTTPException(status_code=400, detail="Invalid conversation ID")
        
        result = await db.conversations.delete_one({"_id": ObjectId(conversation_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {"message": "Conversation deleted"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{conversation_id}/export")
async def export_conversation(
    conversation_id: str,
    format: str = "json",
    db = Depends(get_db)
):
    """Export conversation in different formats"""
    try:
        if not ObjectId.is_valid(conversation_id):
            raise HTTPException(status_code=400, detail="Invalid conversation ID")
        
        conversation = await db.conversations.find_one({"_id": ObjectId(conversation_id)})
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        conversation["_id"] = str(conversation["_id"])
        
        if format == "markdown":
            md_content = f"# {conversation['title']}\n\n"
            for msg in conversation.get("messages", []):
                md_content += f"**{msg['role'].upper()}**: {msg['content']}\n\n"
            return {"format": "markdown", "content": md_content}
        
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
