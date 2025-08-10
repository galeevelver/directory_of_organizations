from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.building import IBuildingRepository
from src.infrastructure.db.repositories.building import SqlAlchemyBuildingRepository
from src.infrastructure.db.session import get_async_session


async def get_building_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> IBuildingRepository:
    return SqlAlchemyBuildingRepository(session)
