from fastapi import HTTPException

from src.domain.repositories.organization import IOrganizationRepository
from src.domain.schemas.organization import OrganizationResponse
from src.domain.services import organization_to_response_limited


class SearchOrganizationsInAreaUseCase:
    """Поиск организаций в радиусе от точки или в прямоугольной области. DTO формируются маппером."""

    def __init__(self, repo: IOrganizationRepository, max_depth: int = 3) -> None:
        self.repo = repo
        self.max_depth = max_depth

    async def execute(
        self,
        lat: float | None,
        lon: float | None,
        radius_km: float | None = None,
        rect_bounds: tuple[float, float, float, float] | None = None,
    ) -> list[OrganizationResponse]:
        if radius_km is not None:
            if lat is None or lon is None:
                raise HTTPException(
                    status_code=422, detail="Для поиска по радиусу необходимы координаты lat и lon"
                )
            models = await self.repo.search_models_in_radius(lat, lon, radius_km)
            return [organization_to_response_limited(m, max_depth=self.max_depth) for m in models]

        if rect_bounds is not None:
            min_lat, max_lat, min_lon, max_lon = rect_bounds
            models = await self.repo.search_models_in_bounds(min_lat, max_lat, min_lon, max_lon)
            return [organization_to_response_limited(m, max_depth=self.max_depth) for m in models]

        raise HTTPException(
            status_code=422, detail="Передайте radius_km или границы прямоугольника"
        )
