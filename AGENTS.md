# AGENTS.md — SaferPassForge Repository Governance & Agent Guidelines

This document establishes non-negotiable guidelines, engineering principles, and operational standards for AI agents and developers working on the **SaferPassForge** codebase.

---

## 1. Official Project Commands

All development tasks must strictly follow these standard commands:

### Virtual Environment Setup & Dependencies
```bash
# Activation (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activation (Linux / macOS)
source .venv/bin/activate

# Install / update pinned dependencies
pip install -r requirements.txt
```

### Application Execution
```bash
# Run local development server with auto-reload
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Testing & Verification
```bash
# Run full test suite
pytest

# Run tests with verbose output
pytest -v

# Run tests targeting a specific file or module
pytest tests/test_config.py
```

---

## 2. Mandatory Software Engineering Principles

Every change must uphold the following core principles:

### 2.1 KISS (Keep It Simple, Stupid)
- Favor straightforward, direct solutions over speculative abstractions or overly clever architectures.
- Implement clear function signatures and keep cognitive complexity low.
- Do not introduce patterns (e.g., CQRS, event sourcing) unless explicitly required by business rules.

### 2.2 YAGNI (You Aren't Gonna Need It)
- Implement strictly what is required for the current MVP scope.
- Do not add "just-in-case" parameters, unused utility functions, or speculative extension points.
- Only introduce third-party libraries listed in `requirements.txt`.

### 2.3 DRY (Don't Repeat Yourself)
- Centralize configuration management in `app/config.py` using `pydantic-settings`.
- Consolidate input validation rules in schema definitions.
- Single-source the entropy calculation logic and password generation routines within the domain layer.

### 2.4 SOLID Architecture & Separation of Concerns
The codebase is structured into three decoupled layers:
1. **Domain (`app/domain`)**:
   - Contains pure business logic, entities, password generation algorithms, and entropy auditors.
   - Absolutely zero dependencies on web frameworks (FastAPI), database engines (SQLAlchemy), or I/O.
2. **Infrastructure (`app/infrastructure`)**:
   - Implements database models, persistence repositories, and external system adapters.
   - Depends only on abstractions defined in the domain layer.
3. **Presentation / API (`app/api`)**:
   - Houses FastAPI routes, endpoint definitions, and request/response schemas.
   - Relies on FastAPI's `Depends` for Dependency Inversion, injecting services and repositories into route handlers.

---

## 3. Strict Git Policy: Conventional Commits One-Liner

All commit messages must be formatted as a single line, adhering strictly to:

```text
<type>(<scope>): <concise description in lowercase>
```

### Rules:
- **Single line only** (no multi-line commit body or footer).
- **Language**: English only.
- **Casing**: Lowercase throughout the entire message (including the first word of the description).
- **Punctuation**: No trailing period.
- **Length**: Maximum 72 characters.
- **Allowed Types**:
  - `feat`: A new feature for the user or system.
  - `fix`: A bug fix.
  - `docs`: Documentation changes only.
  - `style`: Formatting, missing semi-colons, whitespace (no code change).
  - `refactor`: Refactoring production code without behavior changes.
  - `test`: Adding or correcting tests.
  - `chore`: Maintenance, dependencies, build or tooling updates.

### Examples:
- `feat(generator): implement cryptographically secure charset sampling`
- `fix(entropy): correct shannon entropy calculation for short passwords`
- `docs(readme): add architecture diagram and setup instructions`
- `test(config): add unit tests for environment variable validation`

---

## 4. Security-by-Design & Secret Management

- **Absolute Prohibition**: Never commit passwords, API keys, encryption secrets, or local credentials to Git or in code constants.
- **Centralized Environment**: All configurable parameters and secrets must be defined in `.env` (excluded by `.gitignore`) and modeled with static validation in `app/config.py`.
- **Secret Fallback**: Any production secret missing at runtime must fail fast during startup with an informative validation error.
- **Cryptographic Primitives**: Use `secrets` (CSPRNG) rather than `random` for any token or password generation logic.

