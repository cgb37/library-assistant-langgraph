# Project service for CRUD operations

from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from projects.models.project import Project
from typing import Optional

class ProjectService:
    @staticmethod
    async def create_project(db: AsyncSession, name: str, description: Optional[str] = None):
        project = Project(name=name, description=description)
        db.add(project)
        await db.commit()
        await db.refresh(project)
        return project

    @staticmethod
    async def get_projects(db: AsyncSession):
        result = await db.execute(select(Project))
        return result.scalars().all()

    @staticmethod
    async def get_project(db: AsyncSession, project_id: int):
        return await db.get(Project, project_id)

    @staticmethod
    async def update_project(db: AsyncSession, project_id: int, name: str, description: Optional[str] = None):
        project = await db.get(Project, project_id)
        if project:
            project.name = name  # type: ignore
            project.description = description  # type: ignore
            await db.commit()
            await db.refresh(project)
        return project

    @staticmethod
    async def delete_project(db: AsyncSession, project_id: int):
        project = await db.get(Project, project_id)
        if project:
            db.delete(project)  # This is the correct method, no await needed
            await db.commit()
        return project