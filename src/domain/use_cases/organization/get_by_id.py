from typing import Optional

from src.domain.repositories.organization import IOrganizationRepository
from src.domain.schemas.organization import OrganizationResponse
from src.domain.services import organization_to_response_limited


class GetOrganizationByIdUseCase:
    """Получить организацию по ID с отсечкой дерева активностей до 3 уровней."""

    def __init__(self, repo: IOrganizationRepository, max_depth: int = 3) -> None:
        self.repo = repo
        self.max_depth = max_depth

    async def execute(self, organization_id: int) -> Optional[OrganizationResponse]:
        model = await self.repo.get_model_by_id(organization_id)
        if not model:
            return None
        return organization_to_response_limited(model, max_depth=self.max_depth)
