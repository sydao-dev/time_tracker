from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from ...db import database, models
from ...schemas import report as schemas
from ..deps import get_current_user

router = APIRouter()


@router.get("/summary", response_model=schemas.ReportResponse)
def get_summary_report(
        start_date: datetime,
        end_date: datetime,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    entries = db.query(models.TimeEntry).filter(
        models.TimeEntry.user_id == current_user.id,
        models.TimeEntry.start_time >= start_date,
        models.TimeEntry.end_time <= end_date,
        models.TimeEntry.end_time.isnot(None)
    ).all()

    total_time = 0.0
    total_money = 0.0
    projects_data = {}

    for entry in entries:
        duration = (entry.end_time - entry.start_time).total_seconds() / 3600
        rate = entry.project.hourly_rate if entry.project else 0.0
        earned = duration * rate

        total_time += duration
        total_money += earned

        p_name = entry.project.name if entry.project else "Без проєкту"
        if p_name not in projects_data:
            projects_data[p_name] = {"hours": 0.0, "money": 0.0}

        projects_data[p_name]["hours"] += duration
        projects_data[p_name]["money"] += earned

    breakdown = [
        schemas.ProjectSummary(project_name=name, total_hours=data["hours"], total_money=data["money"])
        for name, data in projects_data.items()
    ]

    return schemas.ReportResponse(
        total_time_hours=round(total_time, 2),
        total_earned=round(total_money, 2),
        projects_breakdown=breakdown
    )