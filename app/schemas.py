from enum import Enum
from pydantic import BaseModel, ConfigDict


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
    postcode: str | None = ""
    acquisition_date: str | None = None

    # Lease details
    lease_type: str | None = None
    rent_input_type: str | None = None
    yearly_rent_percent: float | None = None
    monthly_rent: float | None = None
    indexation_type: str | None = None
    indexation_rate: float | None = None
    lease_start: str | None = None
    lease_end: str | None = None

    # Mortgage details
    has_mortgage: bool | None = None
    lender_name: str | None = None
    loan_amount: float | None = None
    interest_rate: float | None = None
    repayment_type: str | None = None
    mortgage_term: float | None = None


class PropertyCreate(PropertyBase):
    """Fields required for creating a new property."""

    pass


class Property(PropertyBase):
    """Fields returned to API clients."""

    id: int

    model_config = ConfigDict(from_attributes=True)