from sqlalchemy import Column, Float, Integer, String

from src.domain.models.base import Base


class Building(Base):
    """Модель здания — содержит адрес и координаты."""

    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True)
    address = Column(String, nullable=False, doc="Полный адрес здания")
    latitude = Column(Float, nullable=False, doc="Широта")
    longitude = Column(Float, nullable=False, doc="Долгота")
