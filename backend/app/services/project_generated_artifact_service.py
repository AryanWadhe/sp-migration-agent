from app.repositories.generated_artifact_repository import (
    GeneratedArtifactRepository
)


class ProjectGeneratedArtifactService:

    @staticmethod
    def get_generated_artifacts(
        db,
        project_id: int
    ):

        return (
            GeneratedArtifactRepository.get_by_project(
                db,
                project_id
            )
        )