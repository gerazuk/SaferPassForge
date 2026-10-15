"""Repository layer for persisting and retrieving password audit records.

Implements the Repository Pattern, decoupling the domain logic and FastAPI
route handlers from the underlying database persistence details.
"""

from typing import Optional

from sqlalchemy import delete, select
from sqlalchemy.orm import Session

from app.config import get_settings
from app.domain.schemas import PasswordStrengthResponse
from app.infrastructure.models import PasswordAuditLog, compute_password_hmac


class PasswordAuditRepository:
    """Repository managing audit records in SQLite."""

    def __init__(self, db: Session, secret_key: Optional[str] = None) -> None:
        """Initializes the repository with a database session and cryptographic key.

        Args:
            db: Active SQLAlchemy database session.
            secret_key: Optional override for the HMAC key; defaults to APP_SECRET_KEY.
        """
        self._db = db
        self._secret_key = secret_key or get_settings().APP_SECRET_KEY

    def create_log(
        self,
        generated: PasswordStrengthResponse,
        secret_key: Optional[str] = None,
    ) -> PasswordAuditLog:
        """Creates and persists an audit entry from a generated password response.

        Never writes plaintext password to disk; hashes it via HMAC-SHA256.

        Args:
            generated: Password generation result schema from domain service.
            secret_key: Optional specific key for HMAC computation.

        Returns:
            PasswordAuditLog: The persisted database record with assigned PK id.
        """
        active_key = secret_key or self._secret_key
        pwd_hash = compute_password_hmac(generated.password, active_key)

        record = PasswordAuditLog(
            context_label=generated.context_label,
            length=generated.length,
            entropy_bits=generated.entropy_bits,
            strength_category=generated.strength_category,
            masked_preview=generated.masked_preview,
            password_hash=pwd_hash,
            created_at=generated.created_at,
        )

        self._db.add(record)
        self._db.commit()
        self._db.refresh(record)
        return record

    def list_recent_logs(self, limit: int = 10) -> list[PasswordAuditLog]:
        """Retrieves the most recent audit logs ordered from newest to oldest.

        Args:
            limit: Maximum number of records to return (defaults to 10).

        Returns:
            list[PasswordAuditLog]: Collection of recent audit entries.
        """
        stmt = (
            select(PasswordAuditLog)
            .order_by(PasswordAuditLog.created_at.desc(), PasswordAuditLog.id.desc())
            .limit(limit)
        )
        return list(self._db.scalars(stmt).all())

    def clear_logs(self) -> int:
        """Deletes all audit records from the database.

        Returns:
            int: Number of deleted rows.
        """
        stmt = delete(PasswordAuditLog)
        result = self._db.execute(stmt)
        self._db.commit()
        return int(result.rowcount)

