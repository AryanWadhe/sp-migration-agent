from sqlalchemy.orm import Session

from app.models.generated_artifact import (
    GeneratedArtifact
)


class GeneratedArtifactRepository:

    @staticmethod
    def create(
    db,
    artifact_id,
    artifact_type,
    model_name,
    storage_path,
    content
) -> GeneratedArtifact:

        generated = GeneratedArtifact(
    artifact_id=artifact_id,
    artifact_type=artifact_type,
    model_name=model_name,
    storage_path=storage_path,
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
        
    @staticmethod
    def get_by_project(
        db: Session,
        project_id: int
    ):

        from app.models.artifact import Artifact

        return (
            db.query(
                GeneratedArtifact
            )
            .join(
                Artifact,
                GeneratedArtifact.artifact_id
                == Artifact.artifact_id
            )
            .filter(
                Artifact.project_id == project_id
            )
            .order_by(
                GeneratedArtifact.generated_artifact_id.desc()
            )
            .all()
        )
    
    
    @staticmethod
    def get_by_artifact_id(
        db,
        artifact_id: int
    ):

        return (
            db.query(
                GeneratedArtifact
            )
            .filter(
                GeneratedArtifact.artifact_id
                == artifact_id
            )
            .order_by(
                GeneratedArtifact.generated_artifact_id.desc()
            )
            .first()
        )