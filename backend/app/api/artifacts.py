from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.artifact import (
    ArtifactCreate,
    ArtifactResponse
)

from app.services.artifact_service import (
    ArtifactService
)

router = APIRouter(
    prefix="/artifacts",
    tags=["Artifacts"]
)


@router.post(
    "",
    response_model=ArtifactResponse
)
def create_artifact(
    payload: ArtifactCreate,
    db: Session = Depends(get_db)
):

    return ArtifactService.create_artifact(
        db,
        payload
    )