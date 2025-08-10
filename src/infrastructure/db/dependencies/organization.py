from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.repositories.organization import IOrganizationRepository
from src.infrastructure.db.repositories.organization import SqlAlchemyOrganizationRepository
from src.infrastructure.db.session import get_async_session


async def get_organization_repository(
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> IOrganizationRepository:
    return SqlAlchemyOrganizationRepository(session)
