from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Self


class ActivityBase(BaseModel):
    name: str = Field(
        ...,
        description="Название вида деятельности",
        json_schema_extra={"example": "Молочная продукция"},
    )
    parent_id: Optional[int] = Field(None, description="ID родительской категории")


class ActivityCreate(ActivityBase):
    pass


class ActivityUpdate(ActivityBase):
    pass


class ActivityResponse(ActivityBase):
    id: int = Field(..., description="Уникальный идентификатор")
    children: List[Self] = Field(default_factory=list, description="Дочерние категории")

    model_config = ConfigDict(from_attributes=True)


ActivityResponse.model_rebuild()
