import logging
import math
from typing import Sequence

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, raiseload

from src.domain.models.activity import Activity
from src.domain.models.building import Building
from src.domain.models.organization import Organization
from src.domain.repositories.organization import IOrganizationRepository

logger = logging.getLogger(__name__)

DEGREE_KM = 111.0
ALL_ATTRS = "*"

organization_load_options = (
    selectinload(Organization.building),
    selectinload(Organization.phones),
    selectinload(Organization.activities)
    .selectinload(Activity.children)
    .selectinload(Activity.children)
    .selectinload(Activity.children),
    raiseload(ALL_ATTRS),
)


class SqlAlchemyOrganizationRepository(IOrganizationRepository):
    """Организации: репозиторий, возвращающий только ORM-модели."""

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_model_by_id(self, organization_id: int) -> Organization | None:
        """Найти организацию по ID."""
        stmt = (
            select(Organization)
            .options(*organization_load_options)
            .where(Organization.id == organization_id)
        )
        result = await self.session.execute(stmt)
        org = result.unique().scalar_one_or_none()
        return org

    async def list_models_by_building_id(self, building_id: int) -> list[Organization]:
        """Список организаций в конкретном здании."""
        stmt = (
            select(Organization)
            .options(*organization_load_options)
            .where(Organization.building_id == building_id)
        )
        result = await self.session.execute(stmt)
        rows: Sequence[Organization] = result.unique().scalars().all()
        return list(rows)

    async def search_models_by_name(self, query: str) -> list[Organization]:
        """Поиск по подстроке (case-insensitive)."""
        ilike_pattern = f"%{query.lower()}%"
        stmt = (
            select(Organization)
            .options(*organization_load_options)
            .where(func.lower(Organization.name).ilike(ilike_pattern))
        )
        result = await self.session.execute(stmt)
        rows: Sequence[Organization] = result.unique().scalars().all()
        return list(rows)

    async def search_models_by_activity_ids(self, activity_ids: list[int]) -> list[Organization]:
        """Поиск организаций по списку activity_id (учитывайте потомков заранее в use-case)."""
        if not activity_ids:
            return []
        stmt = (
            select(Organization)
            .join(Organization.activities)
            .options(*organization_load_options)
            .where(Activity.id.in_(activity_ids))
        )
        result = await self.session.execute(stmt)
        rows: Sequence[Organization] = result.unique().scalars().all()
        return list(rows)

    async def search_models_in_radius(
        self, lat: float, lon: float, radius_km: float
    ) -> list[Organization]:
        """Грубый геопоиск по bounding-box на основе широты/долготы."""
        if radius_km <= 0:
            return []
        lat_delta = radius_km / DEGREE_KM
        lon_factor = max(math.cos(math.radians(lat)), 1e-6)
        lon_delta = radius_km / (DEGREE_KM * lon_factor)

        stmt = (
            select(Organization)
            .join(Organization.building)
            .options(*organization_load_options)
            .where(
                Building.latitude.between(lat - lat_delta, lat + lat_delta),
                Building.longitude.between(lon - lon_delta, lon + lon_delta),
            )
        )
        result = await self.session.execute(stmt)
        rows: Sequence[Organization] = result.unique().scalars().all()
        return list(rows)

    async def search_models_in_bounds(
        self, min_lat: float, max_lat: float, min_lon: float, max_lon: float
    ) -> list[Organization]:
        """Геопоиск по прямоугольной области."""
        if min_lat > max_lat or min_lon > max_lon:
            logger.warning(
                "Некорректные границы bbox: (%s, %s, %s, %s)", min_lat, max_lat, min_lon, max_lon
            )
            return []
        stmt = (
            select(Organization)
            .join(Organization.building)
            .options(*organization_load_options)
            .where(
                Building.latitude.between(min_lat, max_lat),
                Building.longitude.between(min_lon, max_lon),
            )
        )
        result = await self.session.execute(stmt)
        rows: Sequence[Organization] = result.unique().scalars().all()
        return list(rows)
