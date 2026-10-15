"""Domain schemas and data contracts for SaferPassForge.

Defines Pydantic v2 validation models for password generation requests,
strength evaluation responses, and sanitized audit representations.
"""

from datetime import datetime, timezone
from typing import Literal, Optional
from typing_extensions import Self

from pydantic import BaseModel, ConfigDict, Field, model_validator

StrengthCategory = Literal["Weak", "Fair", "Strong", "Very Strong"]


class PasswordGenerateRequest(BaseModel):
    """Input parameters for generating a secure password."""

    model_config = ConfigDict(extra="forbid")

    length: int = Field(
        default=16,
        ge=8,
        le=128,
        description="Password character length between 8 and 128.",
    )
    use_uppercase: bool = Field(
        default=True,
        description="Include uppercase characters (A-Z).",
    )
    use_lowercase: bool = Field(
        default=True,
        description="Include lowercase characters (a-z).",
    )
    use_digits: bool = Field(
        default=True,
        description="Include numeric digits (0-9).",
    )
    use_symbols: bool = Field(
        default=True,
        description="Include special symbols (e.g., !@#$%^&*).",
    )
    exclude_ambiguous: bool = Field(
        default=False,
        description="Exclude visually ambiguous characters (e.g., l, 1, I, O, 0).",
    )
    context_label: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Optional identifier for the secret's purpose (e.g., 'GitHub', 'Banco').",
    )

    @model_validator(mode="after")
    def validate_at_least_one_charset(self) -> Self:
        """Ensures that at least one character category is enabled."""
        if not any(
            [
                self.use_uppercase,
                self.use_lowercase,
                self.use_digits,
                self.use_symbols,
            ]
        ):
            raise ValueError(
                "At least one character group (uppercase, lowercase, digits, symbols) must be enabled."
            )
        return self


class PasswordStrengthResponse(BaseModel):
    """Output schema containing the generated password and security audit metrics."""

    model_config = ConfigDict(from_attributes=True)

    password: str = Field(
        ...,
        description="The generated cryptographically secure plaintext password.",
    )
    length: int = Field(
        ...,
        description="Final character length of the generated password.",
    )
    entropy_bits: float = Field(
        ...,
        description="Shannon-Hartley entropy measured in bits (E = L * log2(R)).",
    )
    strength_category: StrengthCategory = Field(
        ...,
        description="Qualitative security rating based on entropy bits.",
    )
    masked_preview: str = Field(
        ...,
        description="Sanitized visual representation preserving only edge characters.",
    )
    context_label: Optional[str] = Field(
        default=None,
        description="Context or service label attached to this generation.",
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp in UTC when the password was created.",
    )


class PasswordAuditItem(BaseModel):
    """Sanitized representation of a generated password suitable for persistent auditing.

    Never exposes the raw plaintext password, enforcing Security-by-Design.
    """

    model_config = ConfigDict(from_attributes=True)

    id: int = Field(
        ...,
        description="Unique identifier of the audit record.",
    )
    context_label: Optional[str] = Field(
        default=None,
        description="Context or service label attached to this generation.",
    )
    length: int = Field(
        ...,
        description="Character length of the password.",
    )
    entropy_bits: float = Field(
        ...,
        description="Calculated entropy bits.",
    )
    strength_category: StrengthCategory = Field(
        ...,
        description="Qualitative strength categorization.",
    )
    masked_preview: str = Field(
        ...,
        description="Sanitized preview of the password.",
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp in UTC when the audit record was registered.",
    )

