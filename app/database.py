from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.sqltypes import Boolean, Float, Integer, String, Enum as SqlEnum
import os

# Determine an absolute path to the SQLite database so the app uses
# the same file regardless of the current working directory.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "property_planner.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{os.path.abspath(DB_PATH)}"

# For SQLite we need check_same_thread=False for thread safety with FastAPI.
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# The SessionLocal class will be used to instantiate database sessions.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models to inherit from.
Base = declarative_base()


def init_db():
    """Create tables and upgrade schema with any new columns."""
    # Import inside the function to avoid circular imports with models -> database.
    from .models import Property

    Base.metadata.create_all(bind=engine)
    inspector = inspect(engine)
    existing_columns = {col["name"] for col in inspector.get_columns("properties")}

    # Determine columns defined on the Property model but missing in the database.
    model_columns = {
        c.name: c.type for c in Property.__table__.columns if c.name != "id"
    }
    missing = {name: ctype for name, ctype in model_columns.items() if name not in existing_columns}

    if missing:
        with engine.begin() as conn:
            for column, coltype in missing.items():
                if isinstance(coltype, (String, SqlEnum)):
                    sql_type = "TEXT"
                elif isinstance(coltype, Boolean):
                    sql_type = "BOOLEAN"
                elif isinstance(coltype, Integer):
                    sql_type = "INTEGER"
                elif isinstance(coltype, Float):
                    sql_type = "REAL"
                else:
                    sql_type = "TEXT"
                conn.execute(text(f"ALTER TABLE properties ADD COLUMN {column} {sql_type}"))
