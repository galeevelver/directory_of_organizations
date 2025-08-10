from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship

from src.domain.models.base import Base

organization_activity = Table(
    "organization_activity",
    Base.metadata,
    Column("organization_id", ForeignKey("organizations.id", ondelete="CASCADE"), primary_key=True),
    Column("activity_id", ForeignKey("activities.id", ondelete="CASCADE"), primary_key=True),
)


class Organization(Base):
    """Модель организации с привязкой к зданию, телефонам и видам деятельности."""

    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, doc="Название организации")
    building_id = Column(Integer, ForeignKey("buildings.id", ondelete="SET NULL"))

    building = relationship("Building", backref="organizations", lazy="joined")
    activities = relationship("Activity", secondary=organization_activity, backref="organizations")
    phones = relationship(
        "Phone", back_populates="organization", cascade="all, delete-orphan", lazy="joined"
    )
