from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

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