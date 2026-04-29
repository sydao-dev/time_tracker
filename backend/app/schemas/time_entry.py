from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from .tag import TagResponse

class TimeEntryCreate(BaseModel):
    description: str = "No description"
    project_id: Optional[int] = None
    tag_ids: Optional[List[int]] = []

class TimeEntryUpdate(BaseModel):
    end_time: Optional[datetime] = None
    description: Optional[str] = None
    project_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None

class TimeEntryResponse(BaseModel):
    id: int
    description: str
    start_time: datetime
    end_time: Optional[datetime]
    project_id: Optional[int]
    user_id: int
    tags: List[TagResponse] = []

    class Config:
        from_attributes = True