from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Enum as SqlEnum
from .database import Base


class PropertyType(str, Enum):
    """Enumeration for the two property ownership categories."""

    personal = "personal"
    company = "company"


class Property(Base):
    """A real estate asset owned personally or by a company."""

    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    value = Column(Float, nullable=False)
    type = Column(SqlEnum(PropertyType), default=PropertyType.personal, nullable=False)
    address = Column(String, default="", nullable=True)