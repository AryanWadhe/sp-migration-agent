from fastapi import FastAPI

from app.api.health import router as health_router
from app.api.database import router as database_router
from app.core.config import settings
from app.api.projects import router as project_router
from app.api.artifacts import (
    router as artifact_router
)

from app.api.analysis import (
    router as analysis_router
)

from app.api.dbt import (
    router as dbt_router
)

from app.api.generated_artifacts import (
    router as generated_artifact_router
)


app = FastAPI(
    title=settings.APP_NAME
)

app.include_router(
    health_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    database_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    project_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    artifact_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    analysis_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    dbt_router,
    prefix=settings.API_PREFIX
)

app.include_router(
    generated_artifact_router,
    prefix=settings.API_PREFIX
)