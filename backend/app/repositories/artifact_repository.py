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