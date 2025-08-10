from src.domain.repositories.building import IBuildingRepository
from src.domain.schemas.building import BuildingResponse


class GetAllBuildingsUseCase:
    """Получить список всех зданий (репозиторий возвращает модели, маппинг — здесь)."""

    def __init__(self, repo: IBuildingRepository) -> None:
        self.repo = repo

    async def execute(self) -> list[BuildingResponse]:
        models = await self.repo.get_all_models()
        return [BuildingResponse.model_validate(m) for m in models]
