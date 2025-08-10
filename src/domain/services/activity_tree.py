from typing import List, Optional

from src.domain.models.activity import Activity
from src.domain.models.organization import Organization
from src.domain.schemas.activity import ActivityResponse
from src.domain.schemas.building import BuildingResponse
from src.domain.schemas.organization import OrganizationResponse
from src.domain.schemas.phone import PhoneResponse


def activity_to_response_limited(
    activity: Activity, max_depth: int = 3, _level: int = 1
) -> ActivityResponse:
    """Маппинг ORM Activity → DTO с отсечкой children до max_depth без дополнительных SQL-запросов."""
    if _level >= max_depth:
        children: List[ActivityResponse] = []
    else:
        children = [
            activity_to_response_limited(child, max_depth=max_depth, _level=_level + 1)
            for child in getattr(activity, "children", []) or []
        ]
    return ActivityResponse(
        id=activity.id,
        name=activity.name,
        parent_id=activity.parent_id,
        children=children,
    )


def organization_to_response_limited(org: Organization, max_depth: int = 3) -> OrganizationResponse:
    """Маппинг ORM Organization → DTO с отсечкой дерева активностей до max_depth."""
    building: Optional[BuildingResponse] = (
        BuildingResponse.model_validate(org.building) if getattr(org, "building", None) else None
    )
    activities = [
        activity_to_response_limited(a, max_depth=max_depth)
        for a in getattr(org, "activities", []) or []
    ]
    phones = [PhoneResponse.model_validate(p) for p in getattr(org, "phones", []) or []]
    return OrganizationResponse(
        id=org.id,
        name=org.name,
        building=building,
        activities=activities,
        phones=phones,
    )
