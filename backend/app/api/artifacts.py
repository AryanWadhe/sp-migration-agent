from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.artifact import (
    ArtifactCreate,
    ArtifactResponse
)

from app.services.artifact_service import (
    ArtifactService
)

from app.services.artifact_upload_service    import (
    ArtifactUploadService
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
    
    
@router.post(
    "/upload",
    response_model=ArtifactResponse
)
def upload_artifact(
    project_id: int = Form(...),
    artifact_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:

        return (
            ArtifactUploadService.upload(
                db=db,
                project_id=project_id,
                artifact_type=artifact_type,
                file=file
            )
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=400,
            detail=str(ex)
        )