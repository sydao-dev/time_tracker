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