from app.repositories.generated_artifact_repository import (
    GeneratedArtifactRepository
)


class GeneratedArtifactQueryService:

    @staticmethod
    def get_by_id(
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
    
    
    @staticmethod
    def get_by_artifact_id(
        db,
        artifact_id: int
    ):

        artifact = (
            GeneratedArtifactRepository
            .get_by_artifact_id(
                db,
                artifact_id
            )
        )

        if not artifact:

            raise ValueError(
                "Generated artifact not found"
            )

        return artifact