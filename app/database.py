from sqlalchemy import create_engine
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