"""Main entry point for the SaferPassForge application.

Configures FastAPI, lifespan database initialization, API routers,
and static web interface file mounting.
"""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router
from app.config import get_settings
from app.infrastructure.database import init_db

settings = get_settings()

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Manages application startup and shutdown lifecycle events."""
    # Ensure all SQLite database tables exist on startup
    init_db()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description=(
        "Cryptographically secure password generator featuring Shannon-Hartley "
        "entropy auditing and HMAC-SHA256 salted persistence."
    ),
    version="0.1.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Mount API routes
app.include_router(api_router)

# Mount static asset directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", include_in_schema=False)
async def serve_index() -> FileResponse:
    """Serves the integrated single-page user interface."""
    return FileResponse(STATIC_DIR / "index.html")

