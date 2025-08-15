from enum import Enum
from pydantic import BaseModel


class PropertyType(str, Enum):
    """Pydantic version of the property type enum."""

    personal = "personal"
    company = "company"


class PropertyBase(BaseModel):
    """Shared attributes for property creation and retrieval."""

    name: str
    value: float
    type: PropertyType
    address: str | None = ""


class PropertyCreate(PropertyBase):
    """Fields required for creating a new property."""

    pass


class Property(PropertyBase):
    """Fields returned to API clients."""

    id: int

    class Config:
        orm_mode = True