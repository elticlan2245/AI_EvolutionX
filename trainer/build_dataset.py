#!/usr/bin/env python3
"""
Build training dataset from captured conversations
"""
import asyncio
import json
import jsonlines
from pathlib import Path
from datetime import datetime
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

MONGODB_URL = "mongodb://localhost:27017"
DB_NAME = "archllama"
QUALITY_THRESHOLD = 0.7
OUTPUT_DIR = Path("../data/datasets")

async def build_dataset():
    """Build JSONL dataset from MongoDB"""
    logger.info("🔧 Building training dataset...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DB_NAME]
    
    # Query high-quality, unused samples
    cursor = db.training_data.find({
        "quality_score": {"$gte": QUALITY_THRESHOLD},
        "used_in_training": False
    })
    
    samples = []
    async for doc in cursor:
        sample = {
            "instruction": doc["user_message"],
            "output": doc["assistant_message"],
            "metadata": {
                "quality_score": doc["quality_score"],
                "conversation_id": doc["conversation_id"],
                "created_at": doc["created_at"].isoformat()
            }
        }
        samples.append(sample)
    
    if not samples:
        logger.warning("No samples ready for training")
        return None
    
    # Save dataset
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = OUTPUT_DIR / f"dataset_{timestamp}.jsonl"
    
    with jsonlines.open(output_file, 'w') as writer:
        writer.write_all(samples)
    
    logger.info(f"✅ Dataset created: {output_file} ({len(samples)} samples)")
    
    # Mark as used
    sample_ids = [s["metadata"]["conversation_id"] for s in samples]
    await db.training_data.update_many(
        {"conversation_id": {"$in": sample_ids}},
        {"$set": {"used_in_training": True, "training_date": datetime.utcnow()}}
    )
    
    client.close()
    return output_file

if __name__ == "__main__":
    asyncio.run(build_dataset())
