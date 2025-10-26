from motor.motor_asyncio import AsyncIOMotorClient
from typing import Optional
import logging

logger = logging.getLogger(__name__)

client: Optional[AsyncIOMotorClient] = None
db = None

async def init_db():
    global client, db
    try:
        client = AsyncIOMotorClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        db = client.aievolutionx
        await client.admin.command('ping')
        logger.info("✅ MongoDB connected")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        raise

async def close_db():
    global client
    if client:
        client.close()
        logger.info("🔌 MongoDB disconnected")

async def get_db():
    return db
