from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ...db import database, models
from ...schemas import time_entry as schemas
from ..deps import get_current_user

router = APIRouter()

@router.post("/", response_model=schemas.TimeEntryResponse)
def start_time_entry(
        entry: schemas.TimeEntryCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    entry_data = entry.model_dump(exclude_unset=True)
    tag_ids = entry_data.pop("tag_ids", [])

    new_entry = models.TimeEntry(**entry_data, user_id=current_user.id)

    if tag_ids:
        tags = db.query(models.Tag).filter(
            models.Tag.id.in_(tag_ids),
            models.Tag.user_id == current_user.id
        ).all()
        new_entry.tags = tags

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    return new_entry


@router.patch("/{entry_id}", response_model=schemas.TimeEntryResponse)
def stop_or_update_time_entry(
        entry_id: int,
        entry_update: schemas.TimeEntryUpdate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    db_entry = db.query(models.TimeEntry).filter(
        models.TimeEntry.id == entry_id,
        models.TimeEntry.user_id == current_user.id
    ).first()

    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")

    update_data = entry_update.model_dump(exclude_unset=True)

    if "tag_ids" in update_data:
        tag_ids = update_data.pop("tag_ids")
        if tag_ids is not None:
            tags = db.query(models.Tag).filter(
                models.Tag.id.in_(tag_ids),
                models.Tag.user_id == current_user.id
            ).all()
            db_entry.tags = tags

    for key, value in update_data.items():
        setattr(db_entry, key, value)

    db.commit()
    db.refresh(db_entry)
    return db_entry

@router.get("/", response_model=List[schemas.TimeEntryResponse])
def get_time_entries(
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.TimeEntry).filter(models.TimeEntry.user_id == current_user.id)

    if start_date:
        query = query.filter(models.TimeEntry.start_time >= start_date)
    if end_date:
        query = query.filter(models.TimeEntry.start_time <= end_date)

    return query.order_by(models.TimeEntry.start_time.desc()).offset(skip).limit(limit).all()


@router.delete("/{entry_id}", status_code=204)
def delete_time_entry(
        entry_id: int,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    db_entry = db.query(models.TimeEntry).filter(models.TimeEntry.id == entry_id,
                                                 models.TimeEntry.user_id == current_user.id).first()
    if not db_entry:
        raise HTTPException(status_code=404, detail="Запис не знайдено")

    db.delete(db_entry)
    db.commit()
    return None