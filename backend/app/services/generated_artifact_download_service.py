from app.repositories.generated_artifact_repository import (
    GeneratedArtifactRepository
)


class GeneratedArtifactDownloadService:

    @staticmethod
    def get_content(
        db,
        generated_artifact_id: int
    ):

        artifact = (
            GeneratedArtifactRepository.get_by_id(
                db,
                generated_artifact_id
            )
        )

        if not artifact:
            raise ValueError(
                "Generated artifact not found"
            )

        return artifact