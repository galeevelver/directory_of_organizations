from src.domain.repositories.organization import IOrganizationRepository
from src.domain.schemas.organization import OrganizationResponse
from src.domain.services import organization_to_response_limited


class SearchOrganizationsByNameUseCase:
    """Поиск организаций по части названия (case-insensitive)."""

    def __init__(self, repo: IOrganizationRepository, max_depth: int = 3) -> None:
        self.repo = repo
        self.max_depth = max_depth

    async def execute(self, query: str) -> list[OrganizationResponse]:
        models = await self.repo.search_models_by_name(query)
        return [organization_to_response_limited(m, max_depth=self.max_depth) for m in models]
