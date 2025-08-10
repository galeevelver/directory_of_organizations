from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.models.activity import Activity
from src.domain.repositories.activity import IActivityRepository


class SqlAlchemyActivityRepository(IActivityRepository):
    """Виды деятельности: репозиторий, возвращающий ORM-модели."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_all(self) -> list[Activity]:
        stmt = select(Activity)
        result = await self.session.execute(stmt)
        rows: Sequence[Activity] = result.scalars().all()
        return list(rows)

    async def get_descendants(self, activity_id: int, max_depth: int = 3) -> list[int]:
        """Простой DFS по уже загруженному списку (без рекурсивного CTE)."""
        all_acts = await self.get_all()
        children_map: dict[int | None, list[Activity]] = {}
        for act in all_acts:
            children_map.setdefault(act.parent_id, []).append(act)

        descendants: list[int] = []

        def dfs(current_id: int, level: int) -> None:
            if level > max_depth:
                return
            for child in children_map.get(current_id, []):
                descendants.append(child.id)
                dfs(child.id, level + 1)

        dfs(activity_id, 1)
        return descendants
