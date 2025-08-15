from sqlalchemy.orm import Session
from sqlalchemy import func

from . import models, schemas


def get_properties(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve a list of properties."""
    return db.query(models.Property).offset(skip).limit(limit).all()


def create_property(db: Session, property_in: schemas.PropertyCreate):
    """Create and persist a new property."""
    db_property = models.Property(
        name=property_in.name,
        value=property_in.value,
        type=property_in.type,
        address=property_in.address,
    )
    db.add(db_property)
    db.commit()
    db.refresh(db_property)
    return db_property


def portfolio_summary(db: Session):
    """Compute summary statistics for the dashboard."""
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
    total_value = db.query(func.sum(models.Property.value)).scalar() or 0.0
    company_value = (
        db.query(func.sum(models.Property.value))
        .filter(models.Property.type == models.PropertyType.company)
        .scalar()
        or 0.0
    )
    return {
        "personal_count": personal_count,
        "company_count": company_count,
        "total_value": total_value,
        "company_value": company_value,
    }