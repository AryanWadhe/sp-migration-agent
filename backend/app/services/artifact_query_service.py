from app.repositories.artifact_repository import (
    ArtifactRepository
)


class ArtifactQueryService:

    @staticmethod
    def get_by_id(
        db,
        artifact_id: int
    ):

        artifact = (
            ArtifactRepository.get_by_id(
                db,
                artifact_id
            )
        )

        if not artifact:
            raise ValueError(
                "Artifact not found"
            )

        return artifact