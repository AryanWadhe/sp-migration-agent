from pathlib import Path
from hashlib import sha256

from fastapi import UploadFile

from app.models.artifact import (
    Artifact,
    ArtifactType,
    ArtifactStatus
)

from app.repositories.artifact_repository import (
    ArtifactRepository
)


class ArtifactUploadService:

    ALLOWED_EXTENSIONS = {
        ".sql",
        ".prc",
        ".txt"
    }

    @staticmethod
    def upload(
        db,
        project_id: int,
        artifact_type: str,
        file: UploadFile
    ):

        extension = (
            Path(file.filename)
            .suffix
            .lower()
        )

        if extension not in (
            ArtifactUploadService.ALLOWED_EXTENSIONS
        ):
            raise ValueError(
                "Unsupported file type"
            )

        try:

            artifact_enum = (
                ArtifactType(
                    artifact_type.lower()
                )
            )

        except ValueError:

            raise ValueError(
                f"Invalid artifact type: {artifact_type}"
            )

        content = (
            file.file.read()
            .decode("utf-8")
        )

        content_hash = (
            sha256(
                content.encode("utf-8")
            ).hexdigest()
        )

        project_folder = Path(
            f"storage/artifacts/project_{project_id}"
        )

        project_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        file_path = (
            project_folder /
            file.filename
        )

        file_path.write_text(
            content,
            encoding="utf-8"
        )

        artifact = Artifact(
            project_id=project_id,
            file_name=file.filename,
            artifact_type=artifact_enum,
            status=ArtifactStatus.UPLOADED,
            original_content=content,
            file_size=len(content),
            content_hash=content_hash,
            storage_path=str(file_path)
        )

        return (
            ArtifactRepository.create(
                db=db,
                artifact=artifact
            )
        )