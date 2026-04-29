from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserSettingsUpdate(BaseModel):
    pomodoro_focus: Optional[int] = None
    pomodoro_short_break: Optional[int] = None
    pomodoro_long_break: Optional[int] = None

class UserResponse(UserBase):
    id: int
    pomodoro_focus: int
    pomodoro_short_break: int
    pomodoro_long_break: int

    class Config:
        from_attributes = True