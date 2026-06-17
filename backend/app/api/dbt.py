from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database.dependencies import (
    get_db
)

from app.schemas.dbt_generation import (
    DBTGenerationResponse
)

from app.services.artifact_dbt_generation_service import (
    ArtifactDBTGenerationService
)

router = APIRouter(
    prefix="/dbt",
    tags=["DBT"]
)

@router.post(
    "/artifacts/{artifact_id}/generate",
    response_model=DBTGenerationResponse
)
def generate_dbt(
    artifact_id: int,
    db: Session = Depends(get_db)
):

    try:

        result = (
            ArtifactDBTGenerationService.generate(
                db,
                artifact_id
            )
        )

        print("DBT RESULT")
        print(result)

        return result

    except Exception as ex:

        print("ERROR")
        print(type(ex))
        print(ex)

        raise