from fastapi import APIRouter, Query
from typing import List, Dict

router = APIRouter()


@router.get("/cashflow/monthly")
def cashflow_monthly(
    company_id: int,
    from_: str = Query(..., alias="from"),
    to: str = Query(..., alias="to"),
) -> List[Dict[str, float]]:
    """Return mocked monthly cashflow data."""
    return [
        {"month": from_, "cash_in": 0.0, "cash_out": 0.0, "net": 0.0},
        {"month": to, "cash_in": 0.0, "cash_out": 0.0, "net": 0.0},
    ]


@router.get("/properties/stats")
def properties_stats(company_id: int) -> Dict[str, float]:
    """Return mocked statistics about company and personal properties."""
    return {
        "company_count": 0,
        "personal_count": 0,
        "company_portfolio_value": 0.0,
        "personal_portfolio_value": 0.0,
        "company_cash": 0.0,
    }
