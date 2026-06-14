from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database.dependencies import get_db

from app.repositories.project_repository import ProjectRepository

from app.schemas.project import (
    ProjectCreate,
    ProjectResponse
)

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)


@router.post(
    "",
    response_model=ProjectResponse
)
def create_project(
    payload: ProjectCreate,
    db: Session = Depends(get_db)
):

    return ProjectRepository.create(
        db=db,
        name=payload.name,
        description=payload.description
    )