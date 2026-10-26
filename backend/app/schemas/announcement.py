from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class AnnouncementBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    content: str = Field(..., min_length=5)
    category: str = Field(default="General", max_length=50)
    priority: str = Field(default="normal") # "normal", "urgent"
    is_active: bool = True

class AnnouncementCreate(AnnouncementBase):
    pass

class AnnouncementUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    priority: Optional[str] = None
    is_active: Optional[bool] = None

class AnnouncementResponse(AnnouncementBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
