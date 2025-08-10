from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from src.domain.schemas.organization import OrganizationResponse
from src.domain.use_cases.organization.get_by_building import GetOrganizationsByBuildingUseCase
from src.domain.use_cases.organization.get_by_id import GetOrganizationByIdUseCase
from src.domain.use_cases.organization.search_by_activity_tree import (
    SearchOrganizationsByActivityTreeUseCase,
)
from src.domain.use_cases.organization.search_by_name import SearchOrganizationsByNameUseCase
from src.domain.use_cases.organization.search_in_area import SearchOrganizationsInAreaUseCase
from src.infrastructure.db.dependencies.activity import get_activity_repository
from src.infrastructure.db.dependencies.organization import get_organization_repository

router = APIRouter(prefix="/organizations", tags=["Организации"])


@router.get("/search", response_model=List[OrganizationResponse], summary="Поиск по названию")
async def search_by_name(
    query: str = Query(..., description="Часть названия организации"),
    use_case: SearchOrganizationsByNameUseCase = Depends(
        lambda repo=Depends(get_organization_repository): SearchOrganizationsByNameUseCase(repo)
    ),
):
    return await use_case.execute(query)


@router.get("/geo", response_model=List[OrganizationResponse], summary="Геопоиск организаций")
async def search_geo(
    lat: float | None = Query(None, description="Широта"),
    lon: float | None = Query(None, description="Долгота"),
    radius_km: float | None = Query(None, description="Радиус поиска в км"),
    min_lat: float | None = Query(
        None, description="Минимальная широта (нижняя граница прямоугольника)"
    ),
    max_lat: float | None = Query(
        None, description="Максимальная широта (верхняя граница прямоугольника)"
    ),
    min_lon: float | None = Query(
        None, description="Минимальная долгота (левая граница прямоугольника)"
    ),
    max_lon: float | None = Query(
        None, description="Максимальная долгота (правая граница прямоугольника)"
    ),
    use_case: SearchOrganizationsInAreaUseCase = Depends(
        lambda repo=Depends(get_organization_repository): SearchOrganizationsInAreaUseCase(repo)
    ),
):
    rect = (
        (min_lat, max_lat, min_lon, max_lon)
        if None not in (min_lat, max_lat, min_lon, max_lon)
        else None
    )

    if radius_km is not None and lat is not None and lon is not None:
        return await use_case.execute(lat=lat, lon=lon, radius_km=radius_km)

    if rect is not None:
        return await use_case.execute(lat=0, lon=0, rect_bounds=rect)

    raise HTTPException(
        status_code=422, detail="Передайте либо lat/lon + radius_km, либо границы прямоугольника"
    )


@router.get(
    "/activity/{activity_id}",
    response_model=List[OrganizationResponse],
    summary="Поиск по виду деятельности (с учетом вложенности)",
)
async def search_by_activity_tree(
    activity_id: int,
    use_case: SearchOrganizationsByActivityTreeUseCase = Depends(
        lambda org_repo=Depends(get_organization_repository),
        act_repo=Depends(get_activity_repository): SearchOrganizationsByActivityTreeUseCase(
            org_repo, act_repo
        )
    ),
):
    return await use_case.execute(activity_id)


@router.get(
    "/building/{building_id}",
    response_model=List[OrganizationResponse],
    summary="Получить организации по зданию",
)
async def get_organizations_by_building(
    building_id: int,
    use_case: GetOrganizationsByBuildingUseCase = Depends(
        lambda repo=Depends(get_organization_repository): GetOrganizationsByBuildingUseCase(repo)
    ),
):
    return await use_case.execute(building_id)


@router.get(
    "/{organization_id}", response_model=OrganizationResponse, summary="Получить организацию по ID"
)
async def get_organization_by_id(
    organization_id: int,
    use_case: GetOrganizationByIdUseCase = Depends(
        lambda repo=Depends(get_organization_repository): GetOrganizationByIdUseCase(repo)
    ),
):
    org = await use_case.execute(organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org
