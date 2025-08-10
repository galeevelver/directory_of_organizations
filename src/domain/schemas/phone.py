from pydantic import BaseModel, Field, ConfigDict


class PhoneBase(BaseModel):
    phone: str = Field(
        ..., description="Номер телефона", json_schema_extra={"example": "+7-923-666-13-13"}
    )


class PhoneCreate(PhoneBase):
    pass


class PhoneResponse(PhoneBase):
    id: int = Field(..., description="ID телефона")

    model_config = ConfigDict(from_attributes=True)
