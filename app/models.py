from enum import Enum
from sqlalchemy import Column, Integer, String, Float, Boolean, Enum as SqlEnum
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
    postcode = Column(String, default="", nullable=True)
    acquisition_date = Column(String, nullable=True)

    # Lease details
    lease_type = Column(String, nullable=True)
    rent_input_type = Column(String, nullable=True)
    yearly_rent_percent = Column(Float, nullable=True)
    monthly_rent = Column(Float, nullable=True)
    indexation_type = Column(String, nullable=True)
    indexation_rate = Column(Float, nullable=True)
    lease_start = Column(String, nullable=True)
    lease_end = Column(String, nullable=True)

    # Mortgage details
    has_mortgage = Column(Boolean, default=False)
    lender_name = Column(String, nullable=True)
    loan_amount = Column(Float, nullable=True)
    interest_rate = Column(Float, nullable=True)
    repayment_type = Column(String, nullable=True)
    mortgage_term = Column(Float, nullable=True)
