from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.building import Building
from src.domain.repositories.building import IBuildingRepository


class SqlAlchemyBuildingRepository(IBuildingRepository):
    """Здания: репозиторий, возвращающий ORM-модели."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all_models(self) -> list[Building]:
        stmt = select(Building)
        result = await self.session.execute(stmt)
        rows: Sequence[Building] = result.scalars().all()
        return list(rows)
