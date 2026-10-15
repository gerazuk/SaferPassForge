"""Domain services for password generation and entropy audit.

Implements cryptographically secure pseudo-random generation (CSPRNG)
and information-theoretic Shannon-Hartley entropy evaluation.
"""

import math
import secrets
import string
from typing import Optional

from app.domain.schemas import (
    PasswordGenerateRequest,
    PasswordStrengthResponse,
    StrengthCategory,
)

# Standard visual ambiguity set (characters often confused on screens/print)
AMBIGUOUS_CHARACTERS = frozenset("l1IO0o")

# Well-defined symbol set avoiding shell escape hazards while providing high entropy
DEFAULT_SYMBOLS = "!@#$%^&*()-_=+[]{}|;:,.<>?"


class EntropyCalculator:
    """Calculates information-theoretic entropy and classifies password strength.

    Formula:
        E = L * log2(R)
        where:
            E = Entropy in bits
            L = Password length
            R = Size of the character pool (alphabet cardinality)
    """

    # NIST / OWASP aligned entropy thresholds (in bits)
    WEAK_THRESHOLD = 40.0
    FAIR_THRESHOLD = 65.0
    STRONG_THRESHOLD = 80.0

    @classmethod
    def calculate_entropy(cls, length: int, pool_size: int) -> float:
        """Calculates Shannon-Hartley entropy in bits.

        Args:
            length: Number of characters in the password (L).
            pool_size: Number of unique selectable symbols in the pool (R).

        Returns:
            float: Total bits of entropy, rounded to 2 decimal places.
        """
        if length <= 0 or pool_size <= 1:
            return 0.0

        entropy = length * math.log2(pool_size)
        return round(entropy, 2)

    @classmethod
    def classify_strength(cls, entropy_bits: float) -> StrengthCategory:
        """Classifies strength rating based on calculated entropy bits.

        Args:
            entropy_bits: Calculated entropy in bits.

        Returns:
            StrengthCategory: Qualitative rating ('Weak', 'Fair', 'Strong', 'Very Strong').
        """
        if entropy_bits < cls.WEAK_THRESHOLD:
            return "Weak"
        if entropy_bits < cls.FAIR_THRESHOLD:
            return "Fair"
        if entropy_bits < cls.STRONG_THRESHOLD:
            return "Strong"
        return "Very Strong"

    def evaluate(self, length: int, pool_size: int) -> tuple[float, StrengthCategory]:
        """Calculates entropy and returns both metric and qualitative classification."""
        entropy = self.calculate_entropy(length, pool_size)
        category = self.classify_strength(entropy)
        return entropy, category


class PasswordGeneratorService:
    """Domain service for generating cryptographically secure passwords.

    Utilizes strictly the standard library `secrets` module (CSPRNG),
    never `random`, ensuring non-deterministic cryptographic randomness.
    """

    def __init__(self, entropy_calculator: Optional[EntropyCalculator] = None) -> None:
        """Initializes the generator with an entropy calculator dependency."""
        self._entropy_calculator = entropy_calculator or EntropyCalculator()

    @staticmethod
    def _filter_charset(charset: str, exclude_ambiguous: bool) -> str:
        """Removes visually ambiguous characters if requested."""
        if not exclude_ambiguous:
            return charset
        return "".join(ch for ch in charset if ch not in AMBIGUOUS_CHARACTERS)

    @staticmethod
    def _crypto_shuffle(elements: list[str]) -> list[str]:
        """Performs a cryptographically secure in-place Fisher-Yates shuffle.

        Relies on `secrets.randbelow` to eliminate PRNG predictability.
        """
        for i in range(len(elements) - 1, 0, -1):
            j = secrets.randbelow(i + 1)
            elements[i], elements[j] = elements[j], elements[i]
        return elements

    @staticmethod
    def generate_masked_preview(password: str) -> str:
        """Generates a sanitized preview showing only edge characters.

        Example:
            'aB7d9!xZ' -> 'aB****xZ'
            For short passwords (<= 4), all characters are masked.
        """
        length = len(password)
        if length <= 4:
            return "*" * length
        return f"{password[:2]}{'*' * (length - 4)}{password[-2:]}"

    def generate(self, request: PasswordGenerateRequest) -> PasswordStrengthResponse:
        """Generates a secure password matching user specifications.

        Guarantees that at least one character from each requested category
        is present in the resulting password.

        Args:
            request: Validated generation parameters.

        Returns:
            PasswordStrengthResponse: Generated password and security metadata.
        """
        active_pools: list[str] = []

        if request.use_lowercase:
            lowers = self._filter_charset(string.ascii_lowercase, request.exclude_ambiguous)
            if lowers:
                active_pools.append(lowers)

        if request.use_uppercase:
            uppers = self._filter_charset(string.ascii_uppercase, request.exclude_ambiguous)
            if uppers:
                active_pools.append(uppers)

        if request.use_digits:
            digits = self._filter_charset(string.digits, request.exclude_ambiguous)
            if digits:
                active_pools.append(digits)

        if request.use_symbols:
            symbols = self._filter_charset(DEFAULT_SYMBOLS, request.exclude_ambiguous)
            if symbols:
                active_pools.append(symbols)

        if not active_pools:
            raise ValueError("No available characters remain after applying exclusion filters.")

        # Combined pool of available symbols
        combined_pool = "".join(active_pools)
        pool_size = len(set(combined_pool))

        # Guarantee at least 1 character from each active category
        password_chars: list[str] = [
            secrets.choice(pool) for pool in active_pools
        ]

        # Fill the remainder using CSPRNG sampling from the combined pool
        remaining_count = request.length - len(password_chars)
        for _ in range(remaining_count):
            password_chars.append(secrets.choice(combined_pool))

        # Cryptographically secure Fisher-Yates shuffle
        self._crypto_shuffle(password_chars)
        final_password = "".join(password_chars)

        # Calculate entropy and strength classification
        entropy_bits, strength_category = self._entropy_calculator.evaluate(
            length=request.length,
            pool_size=pool_size,
        )

        masked_preview = self.generate_masked_preview(final_password)

        return PasswordStrengthResponse(
            password=final_password,
            length=request.length,
            entropy_bits=entropy_bits,
            strength_category=strength_category,
            masked_preview=masked_preview,
            context_label=request.context_label,
        )

