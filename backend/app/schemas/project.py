from pydantic import BaseModel, Field
from typing import Optional

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Назва проєкту")
    color: str = Field(default="#000000", max_length=7)
    hourly_rate: float = Field(default=0.0, ge=0.0, description="Погодинна ставка у валюті")
    is_archived: bool = False

class ProjectCreate(ProjectBase):
    name: str
    client_id: Optional[int] = None
    color: str = "#000000"
    hourly_rate: float = 0.0

class ProjectResponse(ProjectBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True