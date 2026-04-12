"""SLA113 Database Connection — MongoDB via Motor"""
import logging
from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import get_settings

logger = logging.getLogger(__name__)

_client = None
_db = None


async def connect_to_database():
    global _client, _db
    settings = get_settings()
    _client = AsyncIOMotorClient(settings.MONGO_URL)
    _db = _client[settings.DB_NAME]
    logger.info(f"Connected to MongoDB: {settings.DB_NAME}")


async def close_database_connection():
    global _client
    if _client:
        _client.close()
        logger.info("MongoDB connection closed")


def get_database():
    if _db is None:
        raise RuntimeError("Database not initialized. Call connect_to_database() first.")
    return _db
