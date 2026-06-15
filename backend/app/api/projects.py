from typing import List

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
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


@router.get(
    "",
    response_model=List[ProjectResponse]
)
def get_projects(
    db: Session = Depends(get_db)
):
    return ProjectRepository.get_all(db)

@router.get(
    "/{project_id}",
    response_model=ProjectResponse
)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):

    project = ProjectRepository.get_by_id(
        db,
        project_id
    )

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    return project