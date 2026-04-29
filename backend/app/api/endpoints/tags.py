from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ...db import database, models
from ...schemas import tag as schemas
from ..deps import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.TagResponse)
def create_tag(
    tag: schemas.TagCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    new_tag = models.Tag(**tag.model_dump(), user_id=current_user.id)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag

@router.get("/", response_model=List[schemas.TagResponse])
def get_tags(
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Tag).filter(models.Tag.user_id == current_user.id).all()


@router.delete("/{tag_id}", status_code=204)
def delete_tag(
        tag_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id, models.Tag.user_id == current_user.id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Тег не знайдено")

    db.delete(db_tag)
    db.commit()
    return None