"""
NiyamDrishti FastAPI Application Entry Point
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.core.config import settings
from app.core.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Application startup and shutdown lifecycle."""
    logger.info(
        "NiyamDrishti API starting",
        env=settings.app_env,
        debug=settings.debug,
        ai_available=settings.ai_available,
    )
    yield
    logger.info("NiyamDrishti API shutting down")


app = FastAPI(
    title="NiyamDrishti API",
    description=(
        "AI-powered policy intelligence and student opportunity platform. "
        "Helping students in Andhra Pradesh, Telangana and India discover "
        "scholarships, understand policy changes, and take personalised action."
    ),
    version="1.0.0",
    docs_url="/api/docs" if not settings.is_production else None,
    redoc_url="/api/redoc" if not settings.is_production else None,
    openapi_url="/api/openapi.json" if not settings.is_production else None,
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-Request-ID"],
    expose_headers=["X-Request-ID"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

from app.modules.auth.router import router as auth_router
from app.modules.users.router import router as users_router
from app.modules.profiles.router import router as profiles_router
from app.modules.schemes.router import router as schemes_router
from app.modules.eligibility.router import router as eligibility_router
from app.modules.documents.router import router as documents_router
from app.modules.changelens.router import router as changelens_router
from app.modules.impact.router import router as impact_router
from app.modules.lifemap.router import router as lifemap_router
from app.modules.applications.router import router as applications_router
from app.modules.assistant.router import router as assistant_router
from app.modules.reviews.router import router as reviews_router
from app.modules.notifications.router import router as notifications_router
from app.modules.monitoring.router import router as monitoring_router

API_PREFIX = "/api/v1"

app.include_router(auth_router, prefix=API_PREFIX, tags=["Authentication"])
app.include_router(users_router, prefix=API_PREFIX, tags=["Users"])
app.include_router(profiles_router, prefix=API_PREFIX, tags=["Profiles"])
app.include_router(schemes_router, prefix=API_PREFIX, tags=["Schemes"])
app.include_router(eligibility_router, prefix=API_PREFIX, tags=["Eligibility"])
app.include_router(documents_router, prefix=API_PREFIX, tags=["Documents"])
app.include_router(changelens_router, prefix=API_PREFIX, tags=["ChangeLens"])
app.include_router(impact_router, prefix=API_PREFIX, tags=["Impact"])
app.include_router(lifemap_router, prefix=API_PREFIX, tags=["LifeMap"])
app.include_router(applications_router, prefix=API_PREFIX, tags=["Applications"])
app.include_router(assistant_router, prefix=API_PREFIX, tags=["AI Assistant"])
app.include_router(reviews_router, prefix=API_PREFIX, tags=["Reviews"])
app.include_router(notifications_router, prefix=API_PREFIX, tags=["Notifications"])
app.include_router(monitoring_router, prefix=API_PREFIX, tags=["Monitoring"])


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(
        content={
            "status": "ok",
            "app": settings.app_name,
            "env": settings.app_env,
            "ai_available": settings.ai_available,
        }
    )


@app.get("/", tags=["Root"])
async def root():
    return JSONResponse(
        content={
            "message": "NiyamDrishti API",
            "docs": "/api/docs",
            "health": "/health",
        }
    )
