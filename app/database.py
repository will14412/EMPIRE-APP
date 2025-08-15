from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL; stored in a file for persistence.
SQLALCHEMY_DATABASE_URL = "sqlite:///./property_planner.db"

# For SQLite we need check_same_thread=False for thread safety with FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# The SessionLocal class will be used to instantiate database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models to inherit from.
Base = declarative_base()


def init_db():
    """Create tables and upgrade schema with new columns if missing."""
    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    existing_columns = {
        column["name"] for column in inspector.get_columns("properties")
    }
    required_columns = {
        "postcode",
        "lease_type",
        "rent_input_type",
        "yearly_rent_percent",
        "monthly_rent",
        "indexation_type",
        "indexation_rate",
        "lease_start",
        "lease_end",
        "has_mortgage",
        "lender_name",
        "loan_amount",
        "interest_rate",
        "repayment_type",
        "mortgage_term",
    }
    missing = required_columns - existing_columns
    if missing:
        with engine.begin() as conn:
            for column in missing:
                if column in {
                    "postcode",
                    "lease_type",
                    "rent_input_type",
                    "indexation_type",
                    "lease_start",
                    "lease_end",
                    "lender_name",
                    "repayment_type",
                }:
                    coltype = "TEXT"
                elif column == "has_mortgage":
                    coltype = "BOOLEAN"
                else:
                    coltype = "REAL"
                conn.execute(text(f"ALTER TABLE properties ADD COLUMN {column} {coltype}"))
