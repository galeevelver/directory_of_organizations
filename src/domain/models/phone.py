from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from src.domain.models.base import Base


class Phone(Base):
    """Номер телефона организации."""

    __tablename__ = "phones"

    id = Column(Integer, primary_key=True)
    phone = Column(String, nullable=False)
    organization_id = Column(Integer, ForeignKey("organizations.id", ondelete="CASCADE"))

    organization = relationship("Organization", back_populates="phones")
