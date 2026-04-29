from pydantic import BaseModel, Field

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Назва проєкту")
    color: str = Field(default="#000000", max_length=7)
    hourly_rate: float = Field(default=0.0, ge=0.0, description="Погодинна ставка у валюті")

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True