from typing import Protocol, runtime_checkable
from typing import Optional

from src.domain.models.organization import Organization


@runtime_checkable
class IOrganizationRepository(Protocol):
    async def get_model_by_id(self, organization_id: int) -> Optional[Organization]: ...
    async def list_models_by_building_id(self, building_id: int) -> list[Organization]: ...
    async def search_models_by_name(self, query: str) -> list[Organization]: ...
    async def search_models_by_activity_ids(
        self, activity_ids: list[int]
    ) -> list[Organization]: ...
    async def search_models_in_radius(
        self, lat: float, lon: float, radius_km: float
    ) -> list[Organization]: ...
    async def search_models_in_bounds(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> list[Organization]: ...
