from typing import Protocol, runtime_checkable

from src.domain.models.building import Building


@runtime_checkable
class IBuildingRepository(Protocol):
    async def get_all_models(self) -> list[Building]: ...
