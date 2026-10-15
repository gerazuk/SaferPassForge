"""Unit tests for the infrastructure persistence layer and repository."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.domain.schemas import PasswordGenerateRequest
from app.domain.services import PasswordGeneratorService
from app.infrastructure import (
    Base,
    PasswordAuditLog,
    PasswordAuditRepository,
    compute_password_hmac,
)


@pytest.fixture
def test_db_session() -> Session:
    """Provides an isolated in-memory SQLite database session for testing."""
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=test_engine)
    TestingSession = sessionmaker(bind=test_engine, class_=Session, expire_on_commit=False)
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


def test_compute_password_hmac() -> None:
    """Verifies that HMAC-SHA256 generates a deterministic 64-char hex digest."""
    secret = "super-secret-key-12345"
    h1 = compute_password_hmac("MySecurePass1!", secret)
    h2 = compute_password_hmac("MySecurePass1!", secret)
    h3 = compute_password_hmac("DifferentPass2@", secret)

    assert len(h1) == 64
    assert h1 == h2
    assert h1 != h3


def test_repository_create_and_list_logs(test_db_session: Session) -> None:
    """Verifies that the repository creates logs and retrieves them in descending order."""
    repo = PasswordAuditRepository(db=test_db_session, secret_key="test-secret-key")
    generator = PasswordGeneratorService()

    # Generate 3 test passwords
    for i in range(3):
        req = PasswordGenerateRequest(length=12 + i, context_label=f"Service-{i}")
        generated = generator.generate(req)
        repo.create_log(generated)

    logs = repo.list_recent_logs(limit=10)
    assert len(logs) == 3

    # Ensure descending order (most recent first)
    assert logs[0].context_label == "Service-2"
    assert logs[1].context_label == "Service-1"
    assert logs[2].context_label == "Service-0"

    # Security check: Password plaintext is nowhere in the DB model
    for log in logs:
        assert hasattr(log, "password_hash")
        assert not hasattr(log, "password")
        assert len(log.password_hash) == 64
        assert "*" in log.masked_preview


def test_repository_limit_and_clear_logs(test_db_session: Session) -> None:
    """Verifies limit parameter in list_recent_logs and the clear_logs functionality."""
    repo = PasswordAuditRepository(db=test_db_session, secret_key="test-secret-key")
    generator = PasswordGeneratorService()

    for i in range(5):
        generated = generator.generate(PasswordGenerateRequest(length=10, context_label=f"Label-{i}"))
        repo.create_log(generated)

    # Test limit
    limited = repo.list_recent_logs(limit=2)
    assert len(limited) == 2

    # Test clear_logs
    deleted_count = repo.clear_logs()
    assert deleted_count == 5

    remaining = repo.list_recent_logs()
    assert len(remaining) == 0

