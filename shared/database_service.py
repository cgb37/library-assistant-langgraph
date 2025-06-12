# Shared database service for the Quart app

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from shared.config_service import config_service

MONGO_URL = config_service.get('MONGO_URL')
MONGO_DATABASE = config_service.get('MONGO_DATABASE')

# MongoDB client and database
client = AsyncIOMotorClient(MONGO_URL)
database: AsyncIOMotorDatabase = client[MONGO_DATABASE]

async def get_database():
    """Get the MongoDB database instance"""
    return database

async def close_database():
    """Close the MongoDB client connection"""
    client.close()