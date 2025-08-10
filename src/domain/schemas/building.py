from pydantic import BaseModel, Field, ConfigDict


class BuildingBase(BaseModel):
    address: str = Field(
        ..., description="Адрес здания", json_schema_extra={"example": "г. Москва, ул. Ленина 1"}
    )
    latitude: float = Field(
        ..., ge=-90, le=90, description="Широта", json_schema_extra={"example": 55.7558}
    )
    longitude: float = Field(
        ..., ge=-180, le=180, description="Долгота", json_schema_extra={"example": 37.6173}
    )


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    pass


class BuildingResponse(BuildingBase):
    id: int = Field(..., description="ID здания")

    model_config = ConfigDict(from_attributes=True)
