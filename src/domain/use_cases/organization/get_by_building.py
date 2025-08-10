from src.domain.repositories.organization import IOrganizationRepository
from src.domain.schemas.organization import OrganizationResponse
from src.domain.services import organization_to_response_limited


class GetOrganizationsByBuildingUseCase:
    """Получить организации в здании, DTO формируются маппером."""

    def __init__(self, repo: IOrganizationRepository, max_depth: int = 3) -> None:
        self.repo = repo
        self.max_depth = max_depth

    async def execute(self, building_id: int) -> list[OrganizationResponse]:
        models = await self.repo.list_models_by_building_id(building_id)
        return [organization_to_response_limited(m, max_depth=self.max_depth) for m in models]
