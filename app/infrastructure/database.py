"""Database infrastructure configuration for SaferPassForge.

Implements modern SQLAlchemy 2.0 engine, session factory, declarative base,
and FastAPI dependency injection provider for session management.
"""

from collections.abc import Generator
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import get_settings

settings = get_settings()

# SQLite requires disabling same-thread checks for concurrent async/threaded FastAPI requests
connect_args: dict[str, Any] = {}
if settings.DATABASE_URL.startswith("sqlite"):
    connect_args["check_same_thread"] = False

engine = create_engine(
    settings.DATABASE_URL,
    connect_args=connect_args,
    echo=False,
    future=True,
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=Session,
    expire_on_commit=False,
)


class Base(DeclarativeBase):
    """SQLAlchemy 2.0 declarative base for all infrastructure ORM models."""

    pass


def get_db() -> Generator[Session, None, None]:
    """Provides a managed database session for request lifecycle (FastAPI Depends).

    Yields:
        Session: Active database session.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initializes the database schema by creating all registered tables."""
    Base.metadata.create_all(bind=engine)

