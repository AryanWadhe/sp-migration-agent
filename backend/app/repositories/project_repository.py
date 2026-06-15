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

    @staticmethod
    def get_all(
        db: Session
    ) -> list[Project]:

        return (
            db.query(Project)
            .order_by(Project.project_id)
            .all()
        )
    
    @staticmethod
    def get_by_id(
        db: Session,
        project_id: int
    ) -> Project | None:

        return (
            db.query(Project)
            .filter(Project.project_id == project_id)
            .first()
        )