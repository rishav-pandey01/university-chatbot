from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FeedbackCreate(BaseModel):
    message_id: int
    rating: str = Field(..., description="'helpful' or 'unhelpful'")
    comment: Optional[str] = None

class FeedbackResponse(BaseModel):
    id: int
    message_id: int
    user_id: Optional[int] = None
    rating: str
    comment: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
