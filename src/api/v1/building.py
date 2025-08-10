from fastapi import APIRouter, Depends

from src.domain.schemas.building import BuildingResponse
from src.domain.use_cases.building.get_all import GetAllBuildingsUseCase
from src.infrastructure.db.dependencies.building import get_building_repository

router = APIRouter(prefix="/buildings", tags=["Здания"])


@router.get("", response_model=list[BuildingResponse], summary="Список всех зданий")
async def get_all_buildings(
    use_case: GetAllBuildingsUseCase = Depends(
        lambda repo=Depends(get_building_repository): GetAllBuildingsUseCase(repo)
    ),
):
    return await use_case.execute()
