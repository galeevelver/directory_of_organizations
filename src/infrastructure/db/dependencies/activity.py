from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.activity import IActivityRepository
from src.infrastructure.db.repositories.activity import SqlAlchemyActivityRepository
from src.infrastructure.db.session import get_async_session


async def get_activity_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> IActivityRepository:
    return SqlAlchemyActivityRepository(session)
