from sqlalchemy.orm import Session

from app.models.artifact import Artifact


class ArtifactRepository:

    @staticmethod
    def create(
        db: Session,
        artifact: Artifact
    ) -> Artifact:

        db.add(artifact)
        db.commit()
        db.refresh(artifact)

        return artifact
    
    @staticmethod
    def get_by_id(
        db: Session,
        artifact_id: int
    ) -> Artifact | None:

        return (
            db.query(Artifact)
            .filter(
                Artifact.artifact_id == artifact_id
            )
            .first()
        )
    
    
    @staticmethod
    def get_by_project(
        db: Session,
        project_id: int
    ):

        return (
            db.query(Artifact)
            .filter(
                Artifact.project_id == project_id
            )
            .order_by(
                Artifact.artifact_id.desc()
            )
            .all()
        )