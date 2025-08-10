from src.domain.models.activity import Activity
from src.domain.repositories.activity import IActivityRepository
from src.domain.schemas.activity import ActivityResponse


class GetNestedActivitiesUseCase:
    """Возвращает дерево вложенных активностей (до 3 уровней) по родительской ID."""

    def __init__(self, repo: IActivityRepository) -> None:
        self.repo = repo

    async def execute(self, root_id: int | None = None) -> list[ActivityResponse]:
        all_activities: list[Activity] = await self.repo.get_all()
        children_map: dict[int | None, list[Activity]] = {}
        for act in all_activities:
            children_map.setdefault(act.parent_id, []).append(act)

        def build_tree(parent_id: int | None, level: int = 1) -> list[ActivityResponse]:
            if level > 3:
                return []
            return [
                ActivityResponse(
                    id=child.id,
                    name=child.name,
                    parent_id=child.parent_id,
                    children=build_tree(child.id, level + 1),
                )
                for child in children_map.get(parent_id, [])
            ]

        return build_tree(root_id)
