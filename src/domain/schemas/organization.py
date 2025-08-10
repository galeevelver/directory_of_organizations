from pydantic import BaseModel, Field, ConfigDict
from src.domain.schemas.activity import ActivityResponse
from src.domain.schemas.building import BuildingResponse
from src.domain.schemas.phone import PhoneResponse


class OrganizationBase(BaseModel):
    name: str = Field(
        ..., description="Название организации", json_schema_extra={"example": "ООО Рога и Копыта"}
    )
    building_id: int | None = Field(None, description="ID здания")
    activity_ids: list[int] = Field(
        default_factory=list, description="Список ID видов деятельности"
    )
    phones: list[str] = Field(default_factory=list, description="Список номеров телефонов")


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(OrganizationBase):
    pass


class OrganizationResponse(BaseModel):
    id: int = Field(..., description="ID организации")
    name: str
    building: BuildingResponse | None
    activities: list[ActivityResponse] = Field(default_factory=list)
    phones: list[PhoneResponse] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
