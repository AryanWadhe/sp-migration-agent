from sqlalchemy.orm import Session

from app.repositories.generated_artifact_repository import (
    GeneratedArtifactRepository
)


class GeneratedArtifactService:

    @staticmethod
    def create_dbt_model(
        db: Session,
        artifact_id: int,
        dbt_sql: str
    ):

        return (
            GeneratedArtifactRepository.create(
                db=db,
                artifact_id=artifact_id,
                artifact_type="DBT_MODEL",
                content=dbt_sql
            )
        )