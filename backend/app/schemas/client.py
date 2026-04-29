from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class ClientBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: Optional[EmailStr] = None

class ClientCreate(ClientBase):
    pass

class ClientResponse(ClientBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True