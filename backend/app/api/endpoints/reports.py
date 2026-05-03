from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
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


@router.get("/weekly", response_model=schemas.WeeklyReportResponse)
def get_weekly_report(
        start_date: datetime,
        end_date: datetime,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(get_current_user)
):
    daily_data = {}
    delta = end_date.date() - start_date.date()

    for i in range(delta.days + 1):
        current_day = start_date.date() + timedelta(days=i)
        daily_data[current_day] = {"hours": 0.0, "money": 0.0}

    entries = db.query(models.TimeEntry).filter(
        models.TimeEntry.user_id == current_user.id,
        models.TimeEntry.start_time >= start_date,
        models.TimeEntry.start_time <= end_date,
        models.TimeEntry.end_time.isnot(None)
    ).all()

    for entry in entries:
        entry_date = entry.start_time.date()

        if entry_date in daily_data:
            duration = (entry.end_time - entry.start_time).total_seconds() / 3600
            rate = entry.project.hourly_rate if entry.project else 0.0
            earned = duration * rate

            daily_data[entry_date]["hours"] += duration
            daily_data[entry_date]["money"] += earned

    breakdown = []
    for day, data in daily_data.items():
        breakdown.append(
            schemas.DailySummary(
                date=day.strftime("%Y-%m-%d"),
                weekday=day.strftime("%A"),
                total_hours=round(data["hours"], 2),
                total_money=round(data["money"], 2)
            )
        )

    return schemas.WeeklyReportResponse(
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        daily_breakdown=breakdown
    )
