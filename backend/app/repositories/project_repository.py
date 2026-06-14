from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:

    @staticmethod
    def create(
        db: Session,
        name: str,
        description: str | None
    ) -> Project:

        project = Project(
            name=name,
            description=description
        )

        db.add(project)
        db.commit()
        db.refresh(project)

        return project