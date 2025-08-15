from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models, schemas


def get_properties(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of properties."""
    return db.query(models.Property).offset(skip).limit(limit).all()


def create_property(db: Session, property_in: schemas.PropertyCreate):
    """Create and persist a new property."""
    db_property = models.Property(**property_in.model_dump())
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


def get_property(db: Session, property_id: int):
    """Retrieve a single property by its ID."""
    return db.query(models.Property).filter(models.Property.id == property_id).first()


def update_property(db: Session, property_id: int, property_in: schemas.PropertyCreate):
    """Update an existing property with new data."""
    db_property = get_property(db, property_id)
    if db_property:
        for field, value in property_in.model_dump().items():
            setattr(db_property, field, value)
        db.commit()
        db.refresh(db_property)
    return db_property


def delete_property(db: Session, property_id: int):
    """Delete a property from the database."""
    db_property = get_property(db, property_id)
    if db_property:
        db.delete(db_property)
        db.commit()
    return db_property


def portfolio_summary(db: Session, period: str = "month"):
    """Compute summary statistics for the dashboard.

    Currently only property counts and company portfolio value are persisted.
    Other metrics such as personal portfolio value, company cash and income are
    placeholders until the relevant data models are implemented.
    """

    personal_count = (
        db.query(models.Property)
        .filter(models.Property.type == models.PropertyType.personal)
        .count()
    )
    company_count = (
        db.query(models.Property)
        .filter(models.Property.type == models.PropertyType.company)
        .count()
    )
    company_value = (
        db.query(func.sum(models.Property.value))
        .filter(models.Property.type == models.PropertyType.company)
        .scalar()
        or 0.0
    )

    return {
        "personal_portfolio_value": 0.0,
        "company_value": company_value,
        "company_cash": 0.0,
        "personal_count": personal_count,
        "company_count": company_count,
        "gross_income": 0.0,
        "net_income": 0.0,
        "period": period,
    }