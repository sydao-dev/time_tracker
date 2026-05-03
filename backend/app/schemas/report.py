from pydantic import BaseModel
from typing import List

class ProjectSummary(BaseModel):
    project_name: str
    total_hours: float
    total_money: float

class ReportResponse(BaseModel):
    total_time_hours: float
    total_earned: float
    projects_breakdown: List[ProjectSummary]

class DailySummary(BaseModel):
    date: str
    weekday: str
    total_hours: float
    total_money: float

class WeeklyReportResponse(BaseModel):
    start_date: str
    end_date: str
    daily_breakdown: List[DailySummary]