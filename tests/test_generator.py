"""Unit tests for the password generation engine and entropy audit service."""

import string
import pytest
from pydantic import ValidationError

from app.domain import (
    AMBIGUOUS_CHARACTERS,
    DEFAULT_SYMBOLS,
    EntropyCalculator,
    PasswordGenerateRequest,
    PasswordGeneratorService,
)


def test_should_generate_password_with_exact_requested_length() -> None:
    """Arrange: Prepare service and requests with various valid lengths.
    Act: Generate passwords.
    Assert: The generated password lengths must exactly match the requested lengths.
    """
    # Arrange
    service = PasswordGeneratorService()
    test_lengths = [8, 16, 32, 64, 128]

    for expected_length in test_lengths:
        request = PasswordGenerateRequest(length=expected_length)

        # Act
        response = service.generate(request)

        # Assert
        assert len(response.password) == expected_length
        assert response.length == expected_length


def test_should_include_at_least_one_character_from_each_selected_category() -> None:
    """Arrange: Configure a request with all character categories enabled.
    Act: Generate password.
    Assert: Password contains at least 1 uppercase, 1 lowercase, 1 digit, and 1 symbol.
    """
    # Arrange
    service = PasswordGeneratorService()
    request = PasswordGenerateRequest(
        length=16,
        use_uppercase=True,
        use_lowercase=True,
        use_digits=True,
        use_symbols=True,
    )

    # Act
    response = service.generate(request)

    # Assert
    has_upper = any(c in string.ascii_uppercase for c in response.password)
    has_lower = any(c in string.ascii_lowercase for c in response.password)
    has_digit = any(c in string.digits for c in response.password)
    has_symbol = any(c in DEFAULT_SYMBOLS for c in response.password)

    assert has_upper is True
    assert has_lower is True
    assert has_digit is True
    assert has_symbol is True


def test_should_exclude_ambiguous_characters_when_filter_is_enabled() -> None:
    """Arrange: Configure request with exclude_ambiguous=True.
    Act: Generate multiple passwords across iterations.
    Assert: None of the ambiguous characters ('l', '1', 'I', 'O', '0', 'o') exist in the output.
    """
    # Arrange
    service = PasswordGeneratorService()
    request = PasswordGenerateRequest(
        length=48,
        use_uppercase=True,
        use_lowercase=True,
        use_digits=True,
        use_symbols=True,
        exclude_ambiguous=True,
    )

    # Act & Assert
    for _ in range(15):
        response = service.generate(request)
        for char in response.password:
            assert char not in AMBIGUOUS_CHARACTERS


def test_should_calculate_correct_entropy_and_classify_strength() -> None:
    """Arrange: Initialize EntropyCalculator with known theoretical cardinalities.
    Act: Compute Shannon-Hartley entropy and evaluate classifications.
    Assert: Formula E = L * log2(R) is mathematically exact and thresholds match.
    """
    # Arrange
    calc = EntropyCalculator()

    # Act & Assert - Mathematical formula check:
    # Length = 16, Pool = 64 symbols -> log2(64) = 6.0 -> Entropy = 16 * 6.0 = 96.0 bits
    assert calc.calculate_entropy(length=16, pool_size=64) == 96.0

    # Boundary conditions
    assert calc.calculate_entropy(length=0, pool_size=64) == 0.0
    assert calc.calculate_entropy(length=16, pool_size=1) == 0.0

    # Categorization thresholds (NIST / OWASP)
    assert calc.classify_strength(39.99) == "Weak"
    assert calc.classify_strength(40.0) == "Fair"
    assert calc.classify_strength(64.99) == "Fair"
    assert calc.classify_strength(65.0) == "Strong"
    assert calc.classify_strength(79.99) == "Strong"
    assert calc.classify_strength(80.0) == "Very Strong"


def test_should_raise_validation_error_when_no_charset_is_selected() -> None:
    """Arrange: Disable all character groups.
    Act & Assert: Pydantic model validation must raise ValidationError.
    """
    # Arrange, Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        PasswordGenerateRequest(
            use_uppercase=False,
            use_lowercase=False,
            use_digits=False,
            use_symbols=False,
        )

    assert "At least one character group" in str(exc_info.value)


def test_should_generate_masked_preview_preserving_edges() -> None:
    """Arrange: Provide a sample password.
    Act: Generate masked preview.
    Assert: Only the first 2 and last 2 characters are visible; middle characters are asterisks.
    """
    # Arrange
    service = PasswordGeneratorService()

    # Act
    preview_normal = service.generate_masked_preview("AbCdEfGh1234!@#$")
    preview_short = service.generate_masked_preview("1234")

    # Assert
    assert preview_normal == "Ab************#$"
    assert preview_short == "****"


def test_should_maintain_pure_domain_isolation() -> None:
    """Arrange & Act: Inspect source code of domain layer modules.
    Assert: Neither FastAPI nor SQLAlchemy is imported in the domain layer.
    """
    import app.domain.schemas
    import app.domain.services

    for module in [app.domain.schemas, app.domain.services]:
        source = open(module.__file__, "r", encoding="utf-8").read()
        assert "fastapi" not in source.lower(), f"{module} imports FastAPI!"
        assert "sqlalchemy" not in source.lower(), f"{module} imports SQLAlchemy!"

