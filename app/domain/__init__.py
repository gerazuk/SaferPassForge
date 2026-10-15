"""Domain layer for SaferPassForge.

Houses entities, schemas, entropy calculations, and cryptographic password generation.
Zero dependencies on web framework (FastAPI) or database persistence (SQLAlchemy).
"""

from app.domain.schemas import (
    PasswordAuditItem,
    PasswordGenerateRequest,
    PasswordStrengthResponse,
    StrengthCategory,
)
from app.domain.services import (
    AMBIGUOUS_CHARACTERS,
    DEFAULT_SYMBOLS,
    EntropyCalculator,
    PasswordGeneratorService,
)

__all__ = [
    "PasswordGenerateRequest",
    "PasswordStrengthResponse",
    "PasswordAuditItem",
    "StrengthCategory",
    "EntropyCalculator",
    "PasswordGeneratorService",
    "AMBIGUOUS_CHARACTERS",
    "DEFAULT_SYMBOLS",
]
