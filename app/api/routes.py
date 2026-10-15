"""FastAPI routes for password generation, strength auditing, and health status."""

from typing import Any

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.config import Settings, get_settings
from app.domain.schemas import (
    PasswordAuditItem,
    PasswordGenerateRequest,
    PasswordStrengthResponse,
)
from app.domain.services import PasswordGeneratorService
from app.infrastructure.database import get_db
from app.infrastructure.repository import PasswordAuditRepository

router = APIRouter(prefix="/api/v1", tags=["Passwords & Audit"])


def get_generator_service() -> PasswordGeneratorService:
    """Dependency provider for PasswordGeneratorService."""
    return PasswordGeneratorService()


def get_audit_repository(
    db: Session = Depends(get_db),
    settings: Settings = Depends(get_settings),
) -> PasswordAuditRepository:
    """Dependency provider for PasswordAuditRepository."""
    return PasswordAuditRepository(db=db, secret_key=settings.APP_SECRET_KEY)


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Application Health Check",
)
def health_check(settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    """Returns application operational status and current environment."""
    return {
        "status": "ok",
        "app": settings.APP_NAME,
        "env": settings.APP_ENV,
    }


@router.post(
    "/passwords/generate",
    response_model=PasswordStrengthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Generate Secure Password",
)
def generate_password(
    request: PasswordGenerateRequest,
    generator: PasswordGeneratorService = Depends(get_generator_service),
    repo: PasswordAuditRepository = Depends(get_audit_repository),
) -> PasswordStrengthResponse:
    """Generates a cryptographically secure password and registers an audit log.

    The password is generated using CSPRNG (`secrets`), evaluated for entropy,
    and persisted in SQLite with HMAC-SHA256 hashing.
    """
    generated = generator.generate(request)
    repo.create_log(generated)
    return generated


@router.get(
    "/passwords/history",
    response_model=list[PasswordAuditItem],
    status_code=status.HTTP_200_OK,
    summary="List Audit History",
)
def get_password_history(
    limit: int = Query(default=10, ge=1, le=100, description="Max logs to return"),
    repo: PasswordAuditRepository = Depends(get_audit_repository),
) -> list[PasswordAuditItem]:
    """Retrieves sanitized recent password generation logs (no plaintext passwords)."""
    logs = repo.list_recent_logs(limit=limit)
    return [PasswordAuditItem.model_validate(log) for log in logs]


@router.delete(
    "/passwords/history",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Clear Audit History",
)
def clear_password_history(
    repo: PasswordAuditRepository = Depends(get_audit_repository),
) -> None:
    """Deletes all persisted password generation audit logs from the database."""
    repo.clear_logs()

