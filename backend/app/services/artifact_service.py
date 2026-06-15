from app.models.artifact import Artifact
from app.models.artifact import ArtifactStatus

from app.repositories.artifact_repository import ArtifactRepository

from app.services.hash_service import HashService
from app.services.storage_service import StorageService


class ArtifactService:

    @staticmethod
    def create_artifact(
        db,
        payload
    ):

        content_hash = (
            HashService.generate_sha256(
                payload.original_content
            )
        )

        storage_path = (
            StorageService.save_sql_file(
                payload.project_id,
                payload.file_name,
                payload.original_content
            )
        )

        artifact = Artifact(
            project_id=payload.project_id,
            file_name=payload.file_name,
            artifact_type=payload.artifact_type,
            status=ArtifactStatus.UPLOADED,
            original_content=payload.original_content,
            file_size=len(
                payload.original_content.encode("utf-8")
            ),
            content_hash=content_hash,
            storage_path=storage_path
        )

        return ArtifactRepository.create(
            db,
            artifact
        )