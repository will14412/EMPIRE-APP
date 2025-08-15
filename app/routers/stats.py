from fastapi import APIRouter, Query
from typing import List
from pydantic import BaseModel

router = APIRouter()


class CashflowEntry(BaseModel):
    month: str
    cash_in: float
    cash_out: float
    net: float


class PropertyStats(BaseModel):
    company_count: int
    personal_count: int
    company_portfolio_value: float
    personal_portfolio_value: float
    company_cash: float


@router.get("/cashflow/monthly", response_model=List[CashflowEntry])
def cashflow_monthly(
    company_id: int,
    from_: str = Query(..., alias="from"),
    to: str = Query(..., alias="to"),
) -> List[CashflowEntry]:
    """Return mocked monthly cashflow data."""
    return [
        CashflowEntry(month=from_, cash_in=0.0, cash_out=0.0, net=0.0),
        CashflowEntry(month=to, cash_in=0.0, cash_out=0.0, net=0.0),
    ]


@router.get("/properties/stats", response_model=PropertyStats)
def properties_stats(company_id: int) -> PropertyStats:
    """Return mocked statistics about company and personal properties."""
    return PropertyStats(
        company_count=0,
        personal_count=0,
        company_portfolio_value=0.0,
        personal_portfolio_value=0.0,
        company_cash=0.0,
    )
