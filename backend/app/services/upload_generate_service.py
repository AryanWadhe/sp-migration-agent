from fastapi import UploadFile

from app.services.artifact_upload_service import (
    ArtifactUploadService
)

from app.services.artifact_dbt_generation_service import (
    ArtifactDBTGenerationService
)


class UploadGenerateService:

    @staticmethod
    def upload_and_generate(
        db,
        project_id: int,
        artifact_type: str,
        file: UploadFile
    ):

        artifact = (
            ArtifactUploadService.upload(
                db=db,
                project_id=project_id,
                artifact_type=artifact_type,
                file=file
            )
        )

        generated = (
            ArtifactDBTGenerationService.generate(
                db=db,
                artifact_id=artifact.artifact_id
            )
        )

        return {
            "artifact_id":
                artifact.artifact_id,

            "generated_artifact_id":
                generated[
                    "generated_artifact_id"
                ],

            "target_model":
                generated[
                    "target_model"
                ],

            "dbt_sql":
                generated[
                    "dbt_sql"
                ]
        }