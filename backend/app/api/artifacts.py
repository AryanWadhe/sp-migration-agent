from fastapi import APIRouter
from fastapi import Depends
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from typing import List
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
from app.services.artifact_query_service import (
    ArtifactQueryService
)
from app.services.upload_generate_service import (
    UploadGenerateService
)

from app.schemas.upload_generate_response import (
    UploadGenerateResponse
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
        
@router.get(
    "/{artifact_id}",
    response_model=ArtifactResponse
)
def get_artifact(
    artifact_id: int,
    db: Session = Depends(get_db)
):

    try:

        return (
            ArtifactQueryService.get_by_id(
                db,
                artifact_id
            )
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )
        

@router.get(
    "/project/{project_id}",
    response_model=List[ArtifactResponse]
)
def get_project_artifacts(
    project_id: int,
    db: Session = Depends(get_db)
):

    return (
        ProjectArtifactService.get_artifacts(
            db,
            project_id
        )
    )

    
@router.post(
    "/upload-and-generate",
    response_model=UploadGenerateResponse
)
def upload_and_generate(
    project_id: int = Form(...),
    artifact_type: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:

        return (
            UploadGenerateService.upload_and_generate(
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