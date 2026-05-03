from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ...db import database, models
from ...schemas import time_entry as schemas
from ..deps import get_current_user
import csv
import io
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import joinedload

router = APIRouter()


@router.post("/", response_model=schemas.TimeEntryResponse)
def start_time_entry(
        entry: schemas.TimeEntryCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    active_entry = db.query(models.TimeEntry).filter(
        models.TimeEntry.user_id == current_user.id,
        models.TimeEntry.end_time.is_(None)
    ).first()

    if active_entry:
        active_entry.end_time = datetime.now(timezone.utc)
        db.add(active_entry)

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


@router.get("/export/csv")
def export_time_entries_csv(
        start_date: datetime,
        end_date: datetime,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    entries = db.query(models.TimeEntry).options(
        joinedload(models.TimeEntry.project).joinedload(models.Project.client)
    ).filter(
        models.TimeEntry.user_id == current_user.id,
        models.TimeEntry.start_time >= start_date,
        models.TimeEntry.start_time <= end_date
    ).order_by(models.TimeEntry.start_time.asc()).all()

    output = io.StringIO()
    writer = csv.writer(output, delimiter=',', quoting=csv.QUOTE_MINIMAL)

    writer.writerow([
        "Date", "Client", "Project", "Description",
        "Start Time", "End Time", "Duration (Hours)",
        "Hourly Rate", "Total Earned"
    ])

    for entry in entries:
        duration_hours = 0.0
        if entry.end_time:
            duration_hours = (entry.end_time - entry.start_time).total_seconds() / 3600

        project_name = entry.project.name if entry.project else "No Project"
        client_name = entry.project.client.name if (entry.project and entry.project.client) else "-"
        rate = entry.project.hourly_rate if entry.project else 0.0
        earned = duration_hours * rate

        writer.writerow([
            entry.start_time.strftime("%Y-%m-%d"),
            client_name,
            project_name,
            entry.description,
            entry.start_time.strftime("%H:%M:%S"),
            entry.end_time.strftime("%H:%M:%S") if entry.end_time else "Running",
            round(duration_hours, 2),
            rate,
            round(earned, 2)
        ])

    output.seek(0)

    filename = f"timesheet_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )