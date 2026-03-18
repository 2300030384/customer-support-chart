from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from typing import Optional, Any
from app.config import settings
import logging

logger = logging.getLogger(__name__)


class Database:
    """MongoDB database connection handler (Synchronous for deployment compatibility)"""
    
    client: Optional[MongoClient] = None
    db: Optional[Any] = None


async def connect_to_mongo():
    """Connect to MongoDB"""
    try:
        Database.client = MongoClient(
            settings.mongodb_url,
            serverSelectionTimeoutMS=5000,
            connectTimeoutMS=10000,
            retryWrites=True,
            w='majority'
        )
        # Verify connection
        Database.client.admin.command('ping')
        Database.db = Database.client[settings.mongodb_db_name]
        logger.info("✓ Connected to MongoDB")
        
        # Create indexes
        create_indexes()
    except ServerSelectionTimeoutError as e:
        logger.error(f"✗ Failed to connect to MongoDB: {e}")
        raise
    except Exception as e:
        logger.error(f"✗ MongoDB connection error: {e}")
        raise


async def close_mongo_connection():
    """Close MongoDB connection"""
    if Database.client:
        Database.client.close()
        logger.info("✓ Closed MongoDB connection")


def create_indexes():
    """Create MongoDB indexes for better performance"""
    db = Database.db
    if db is None:
        logger.warning("⚠ Database not connected, skipping index creation")
        return
    
    try:
        # Conversations collection indexes
        conversations_col = db["conversations"]
        conversations_col.create_index("thread_id", unique=True)
        conversations_col.create_index("platform")
        conversations_col.create_index("created_at")
        conversations_col.create_index("escalation_detected")
        
        logger.info("✓ MongoDB indexes created")
    except Exception as e:
        logger.warning(f"⚠ Could not create indexes: {e}")


def get_database() -> Any:
    """Get database instance"""
    return Database.db