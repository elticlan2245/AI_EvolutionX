from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
import logging

from app.config.settings import settings

logger = logging.getLogger(__name__)

# MongoDB client
client: AsyncIOMotorClient = None
db = None

async def init_db():
    """Initialize database connection"""
    global client, db
    
    try:
        client = AsyncIOMotorClient(settings.mongodb_url)
        db = client[settings.database_name]  # ✅ Ahora usa el nombre correcto
        
        # Test connection
        await client.admin.command('ping')
        
        logger.info(f"✅ MongoDB connected: {settings.database_name}")
        
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
        raise

async def close_db():
    """Close database connection"""
    global client
    
    if client:
        client.close()
        logger.info("�� MongoDB connection closed")

def get_db():
    """Dependency for getting database"""
    return db
