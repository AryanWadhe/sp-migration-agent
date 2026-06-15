from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.schemas.analysis_run import (
    AnalysisRunResponse
)

from app.services.parser_analysis_service import (
    ParserAnalysisService
)

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"]
)


@router.post(
    "/artifacts/{artifact_id}/parse",
    response_model=AnalysisRunResponse
)
def parse_artifact(
    artifact_id: int,
    db: Session = Depends(get_db)
):

    try:

        return (
            ParserAnalysisService.analyze_artifact(
                db,
                artifact_id
            )
        )

    except ValueError as ex:

        raise HTTPException(
            status_code=404,
            detail=str(ex)
        )