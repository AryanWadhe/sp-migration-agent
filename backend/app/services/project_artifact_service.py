from app.repositories.artifact_repository import (
    ArtifactRepository
)


class ProjectArtifactService:

    @staticmethod
    def get_artifacts(
        db,
        project_id: int
    ):

        return (
            ArtifactRepository.get_by_project(
                db,
                project_id
            )
        )