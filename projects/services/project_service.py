# Project service for CRUD operations

from motor.motor_asyncio import AsyncIOMotorDatabase
from projects.models.project import Project, ProjectCreate, ProjectUpdate
from typing import Optional, List
from bson import ObjectId

class ProjectService:
    def __init__(self, database: AsyncIOMotorDatabase):
        self.collection = database.projects

    async def create_project(self, project_data: ProjectCreate) -> Project:
        project_dict = project_data.dict()
        result = await self.collection.insert_one(project_dict)
        created_project = await self.collection.find_one({"_id": result.inserted_id})
        created_project["_id"] = str(created_project["_id"])
        return Project(**created_project)

    async def get_projects(self) -> List[Project]:
        projects = []
        async for project_doc in self.collection.find():
            project_doc["_id"] = str(project_doc["_id"])
            projects.append(Project(**project_doc))
        return projects

    async def get_project(self, project_id: str) -> Optional[Project]:
        if not ObjectId.is_valid(project_id):
            return None
        project_doc = await self.collection.find_one({"_id": ObjectId(project_id)})
        if project_doc:
            project_doc["_id"] = str(project_doc["_id"])
            return Project(**project_doc)
        return None

    async def update_project(self, project_id: str, project_data: ProjectUpdate) -> Optional[Project]:
        if not ObjectId.is_valid(project_id):
            return None
        
        update_dict = {k: v for k, v in project_data.dict().items() if v is not None}
        if not update_dict:
            return await self.get_project(project_id)
            
        await self.collection.update_one(
            {"_id": ObjectId(project_id)}, 
            {"$set": update_dict}
        )
        return await self.get_project(project_id)

    async def delete_project(self, project_id: str) -> bool:
        if not ObjectId.is_valid(project_id):
            return False
        result = await self.collection.delete_one({"_id": ObjectId(project_id)})
        return result.deleted_count > 0