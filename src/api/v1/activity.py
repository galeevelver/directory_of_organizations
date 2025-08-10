from fastapi import APIRouter, Depends, Query
from typing import List

from src.domain.schemas.activity import ActivityResponse
from src.domain.use_cases.activity.get_nested_activities import GetNestedActivitiesUseCase
from src.infrastructure.db.dependencies.activity import get_activity_repository

router = APIRouter(prefix="/activities", tags=["Виды деятельности"])


@router.get(
    "",
    response_model=List[ActivityResponse],
    summary="Дерево видов деятельности",
    description="Вернуть дерево видов деятельности с вложенностью до 3 уровней. Если указан root_id — вернуть поддерево.",
)
async def get_nested_activities(
    root_id: int | None = Query(None, description="ID корневой категории"),
    use_case: GetNestedActivitiesUseCase = Depends(
        lambda repo=Depends(get_activity_repository): GetNestedActivitiesUseCase(repo)
    ),
):
    return await use_case.execute(root_id)
