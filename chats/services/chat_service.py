# Chat service for CRUD operations

from motor.motor_asyncio import AsyncIOMotorDatabase
from chats.models.chat import Chat, ChatCreate
from typing import Optional, List
from bson import ObjectId
from datetime import datetime

class ChatService:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.chats

    async def create_chat(self, chat_data: ChatCreate) -> Chat:
        chat_dict = chat_data.dict()
        chat_dict["created_at"] = datetime.utcnow()
        result = await self.collection.insert_one(chat_dict)
        created_chat = await self.collection.find_one({"_id": result.inserted_id})
        created_chat["_id"] = str(created_chat["_id"])
        return Chat(**created_chat)

    async def get_chats(self, limit: int = 50) -> List[Chat]:
        chats = []
        async for chat_doc in self.collection.find().sort("created_at", -1).limit(limit):
            chat_doc["_id"] = str(chat_doc["_id"])
            chats.append(Chat(**chat_doc))
        return chats

    async def get_chat(self, chat_id: str) -> Optional[Chat]:
        if not ObjectId.is_valid(chat_id):
            return None
        chat_doc = await self.collection.find_one({"_id": ObjectId(chat_id)})
        if chat_doc:
            chat_doc["_id"] = str(chat_doc["_id"])
            return Chat(**chat_doc)
        return None

    async def delete_chat(self, chat_id: str) -> bool:
        if not ObjectId.is_valid(chat_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(chat_id)})
        return result.deleted_count > 0
