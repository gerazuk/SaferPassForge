"""SQLAlchemy persistence models for security audit logging.

Enforces Security-by-Design by persisting only cryptographic hashes and
masked previews, never raw plaintext passwords.
"""

import hashlib
import hmac
from datetime import datetime, timezone
from typing import Optional

from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.database import Base


def compute_password_hmac(password: str, secret_key: str) -> str:
    """Computes an HMAC-SHA256 hash of the password using the application secret key.

    Enables uniqueness/integrity verification without storing plaintext secrets.

    Args:
        password: Raw generated password string.
        secret_key: Secret key from application settings.

    Returns:
        str: 64-character hexadecimal HMAC digest.
    """
    return hmac.new(
        key=secret_key.encode("utf-8"),
        msg=password.encode("utf-8"),
        digestmod=hashlib.sha256,
    ).hexdigest()


class PasswordAuditLog(Base):
    """Audit log entry for generated passwords.

    Captures security metadata and salted hash for accountability and audit trails.
    """

    __tablename__ = "password_audit_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
        autoincrement=True,
    )
    context_label: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        index=True,
    )
    length: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )
    entropy_bits: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    strength_category: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )
    masked_preview: Mapped[str] = mapped_column(
        String(130),
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"<PasswordAuditLog(id={self.id}, context='{self.context_label}', "
            f"length={self.length}, entropy={self.entropy_bits} bits, "
            f"category='{self.strength_category}')>"
        )

