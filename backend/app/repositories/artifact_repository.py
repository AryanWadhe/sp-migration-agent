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