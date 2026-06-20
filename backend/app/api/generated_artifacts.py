from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from typing import List

from sqlalchemy.orm import Session

from app.database.dependencies import (
    get_db
)

from app.schemas.generated_artifact import (
    GeneratedArtifactResponse
)

from app.services.generated_artifact_query_service import (
    GeneratedArtifactQueryService
)

from fastapi.responses import Response

from app.services.generated_artifact_download_service import (
    GeneratedArtifactDownloadService
)


from app.services.project_generated_artifact_service import (
    ProjectGeneratedArtifactService
)

router = APIRouter(
    prefix="/generated-artifacts",
    tags=["Generated Artifacts"]
)


@router.get(
    "/{generated_artifact_id}",
    response_model=GeneratedArtifactResponse
)
def get_generated_artifact(
    generated_artifact_id: int,
    db: Session = Depends(get_db)
):

    try:

        return (
            GeneratedArtifactQueryService.get_by_id(
                db,
                generated_artifact_id
            )
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )

@router.get(
    "/{generated_artifact_id}/download"
)
def download_generated_artifact(
    generated_artifact_id: int,
    db: Session = Depends(get_db)
):

    try:

        artifact = (
            GeneratedArtifactDownloadService.get_content(
                db,
                generated_artifact_id
            )
        )

        return Response(
            content=artifact.content,
            media_type="text/plain",
            headers={
                "Content-Disposition":
                    f'attachment; filename="generated_{generated_artifact_id}.sql"'
            }
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )
        
        
@router.get(
    "/project/{project_id}",
    response_model=List[
        GeneratedArtifactResponse
    ]
)
def get_project_generated_artifacts(
    project_id: int,
    db: Session = Depends(get_db)
):

    return (
        ProjectGeneratedArtifactService
        .get_generated_artifacts(
            db,
            project_id
        )
    )
    

@router.get(
    "/artifact/{artifact_id}",
    response_model=
    GeneratedArtifactResponse
)
def get_by_artifact(
    artifact_id: int,
    db: Session = Depends(get_db)
):

    try:

        return (
            GeneratedArtifactQueryService
            .get_by_artifact_id(
                db,
                artifact_id
            )
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )