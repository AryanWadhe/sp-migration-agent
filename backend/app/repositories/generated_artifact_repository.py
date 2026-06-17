from sqlalchemy.orm import Session

from app.models.generated_artifact import (
    GeneratedArtifact
)


class GeneratedArtifactRepository:

    @staticmethod
    def create(
        db: Session,
        artifact_id: int,
        artifact_type: str,
        content: str
    ) -> GeneratedArtifact:

        generated = GeneratedArtifact(
            artifact_id=artifact_id,
            artifact_type=artifact_type,
            content=content
        )

        db.add(generated)
        db.commit()
        db.refresh(generated)

        return generated

    @staticmethod
    def get_by_id(
        db: Session,
        generated_artifact_id: int
    ) -> GeneratedArtifact | None:

        return (
            db.query(
                GeneratedArtifact
            )
            .filter(
                GeneratedArtifact.generated_artifact_id
                == generated_artifact_id
            )
            .first()
        )