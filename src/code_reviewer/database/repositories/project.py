from uuid import UUID

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ..models import ProjectOrm

from ...core.base import CRUDRepository
from ...core.schemas import Project
from ...core.exceptions import (
    CreationError,
    ReadingError,
    UpdateError,
    DeletionError
)


class SQLProjectRepository(CRUDRepository[Project]):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(self, project: Project) -> Project:
        try:
            stmt = (
                insert(ProjectOrm)
                .values(**project.model_dump())
                .returning(ProjectOrm)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            project_orm = result.scalar_one()
            return Project.model_validate(project_orm)
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise CreationError(f"Error while project creation: {e}") from e

    async def read(self, id: UUID) -> Project | None:
        try:
            stmt = (
                select(ProjectOrm)
                .where(ProjectOrm.id == id)
            )
            result = await self.session.execute(stmt)
            project_orm = result.scalar_one_or_none()
            return Project.model_validate(project_orm) if project_orm else None
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ReadingError(f"Error while reading project: {e}") from e

    async def update(self, id: UUID, **kwargs) -> Project | None:
        try:
            stmt = (
                update(ProjectOrm)
                .values(**kwargs)
                .where(ProjectOrm.id == id)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            project_orm = result.scalar_one_or_none()
            return Project.model_validate(project_orm) if project_orm else None
        except SQLAlchemyError as e:
            raise UpdateError(f"Error while update project: {e}") from e

    async def delete(self, id: UUID) -> bool:
        try:
            stmt = (
                delete(ProjectOrm)
                .where(ProjectOrm.id == id)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.rowcount > 0
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise DeletionError(f"Error while delete project: {e}") from e
