from pydantic import BaseModel, Field

class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: str = Field(default="#808080", max_length=7)

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True