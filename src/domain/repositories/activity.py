from typing import Protocol, runtime_checkable

from src.domain.models.activity import Activity


@runtime_checkable
class IActivityRepository(Protocol):
    async def get_all(self) -> list[Activity]: ...
    async def get_descendants(self, activity_id: int, max_depth: int = 3) -> list[int]: ...
