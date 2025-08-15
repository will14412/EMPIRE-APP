import sys
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(str(Path(__file__).resolve().parents[1]))

from app import models, schemas
from app.main import create_property_api


@pytest.fixture()
def db_session(tmp_path):
    db_path = tmp_path / "test.db"
    engine = create_engine(f"sqlite:///{db_path}", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        models.Base.metadata.drop_all(bind=engine)


@pytest.mark.parametrize("rent_input_type,has_mortgage", [
    ("currency", False),
    ("currency", True),
    ("percent", False),
    ("percent", True),
])
def test_create_property_various_inputs(db_session, rent_input_type, has_mortgage):
    payload = {
        "postcode": "AB1 1CD",
        "address": "1 Street",
        "name": f"Property {rent_input_type} {has_mortgage}",
        "value": 100000.0,
        "acquisition_date": "2024-01-01",
        "type": "personal",
        "lease_type": "ast",
    }

    if rent_input_type == "percent":
        payload.update({
            "rent_input_type": "percent",
            "yearly_rent_percent": 12.0,
            "monthly_rent": 1000.0,
        })
    else:
        payload.update({
            "rent_input_type": "currency",
            "monthly_rent": 1000.0,
        })

    if has_mortgage:
        payload.update({
            "has_mortgage": True,
            "lender_name": "Bank",
            "loan_amount": 50000.0,
            "interest_rate": 3.5,
            "repayment_type": "interest_only",
            "mortgage_term": 25,
        })
    else:
        payload.update({
            "has_mortgage": False,
            "lender_name": None,
            "loan_amount": None,
            "interest_rate": None,
            "repayment_type": None,
            "mortgage_term": None,
        })

    property_in = schemas.PropertyCreate(**payload)
    result = create_property_api(property_in, db_session)
    assert result.name == payload["name"]
    assert result.value == payload["value"]
    assert db_session.query(models.Property).count() == 1
