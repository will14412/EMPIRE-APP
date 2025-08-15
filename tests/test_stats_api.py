from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_properties_stats():
    response = client.get("/properties/stats", params={"company_id": 1})
    assert response.status_code == 200
    data = response.json()
    assert set(data.keys()) == {
        "company_count",
        "personal_count",
        "company_portfolio_value",
        "personal_portfolio_value",
        "company_cash",
    }


def test_cashflow_monthly():
    response = client.get(
        "/cashflow/monthly",
        params={"company_id": 1, "from": "2024-01", "to": "2024-02"},
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert data[0]["month"] == "2024-01"
    assert data[1]["month"] == "2024-02"
