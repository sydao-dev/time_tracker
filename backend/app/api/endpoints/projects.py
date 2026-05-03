from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import database, models
from ...schemas import project as project_schemas
from ..deps import get_current_user

router = APIRouter()

@router.post("/", response_model=project_schemas.ProjectResponse)
def create_project(
    project: project_schemas.ProjectCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_project = models.Project(**project.model_dump(), user_id=current_user.id)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    return new_project


@router.get("/", response_model=List[project_schemas.ProjectResponse])
def get_projects(
        include_archived: bool = False,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Project).filter(models.Project.user_id == current_user.id)

    if not include_archived:
        query = query.filter(models.Project.is_archived == False)

    return query.all()


@router.patch("/{project_id}", response_model=project_schemas.ProjectResponse)
def update_project(
        project_id: int,
        project_update: project_schemas.ProjectBase,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id,
                                                 models.Project.user_id == current_user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Проєкт не знайдено")

    for key, value in project_update.model_dump(exclude_unset=True).items():
        setattr(db_project, key, value)

    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}", status_code=204)
def delete_project(
        project_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    db_project = db.query(models.Project).filter(models.Project.id == project_id,
                                                 models.Project.user_id == current_user.id).first()
    if not db_project:
        raise HTTPException(status_code=404, detail="Проєкт не знайдено")

    db.delete(db_project)
    db.commit()
    return None