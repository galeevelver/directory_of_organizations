from src.domain.repositories.activity import IActivityRepository
from src.domain.repositories.organization import IOrganizationRepository
from src.domain.schemas.organization import OrganizationResponse
from src.domain.services import organization_to_response_limited


class SearchOrganizationsByActivityTreeUseCase:
    """Поиск по ID вида деятельности и всем его потомкам (вложенность до 3 уровней)."""

    def __init__(
        self,
        org_repo: IOrganizationRepository,
        activity_repo: IActivityRepository,
        max_depth: int = 3,
    ) -> None:
        self.org_repo = org_repo
        self.activity_repo = activity_repo
        self.max_depth = max_depth

    async def execute(self, activity_id: int) -> list[OrganizationResponse]:
        descendant_ids = await self.activity_repo.get_descendants(activity_id, max_depth=3)
        models = await self.org_repo.search_models_by_activity_ids([activity_id] + descendant_ids)
        return [organization_to_response_limited(m, max_depth=self.max_depth) for m in models]
