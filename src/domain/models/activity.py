from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.domain.models.base import Base


class Activity(Base):
    __tablename__ = "activities"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False, doc="Название вида деятельности")
    parent_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("activities.id", ondelete="CASCADE")
    )

    parent: Mapped[Optional["Activity"]] = relationship(
        "Activity", remote_side=[id], back_populates="children"
    )
    children: Mapped[list["Activity"]] = relationship(
        back_populates="parent", cascade="all, delete-orphan"
    )
