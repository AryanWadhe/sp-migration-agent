from sqlalchemy.orm import Session

from app.repositories.generated_artifact_repository import (
    GeneratedArtifactRepository
)


class GeneratedArtifactService:

    @staticmethod
    def create_dbt_model(
        db,
        artifact_id,
        model_name,
        storage_path,
        dbt_sql
    ):

        return (
            GeneratedArtifactRepository.create(
                 db=db,
                artifact_id=artifact_id,
                artifact_type="DBT_MODEL",
                model_name=model_name,
                storage_path=storage_path,
                content=dbt_sql
            )
        )