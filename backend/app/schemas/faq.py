from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class FAQBase(BaseModel):
    category: str = Field(..., min_length=2, max_length=50)
    question: str = Field(..., min_length=5, max_length=300)
    answer: str = Field(..., min_length=5)
    keywords: Optional[str] = None

class FAQCreate(FAQBase):
    pass

class FAQUpdate(BaseModel):
    category: Optional[str] = None
    question: Optional[str] = None
    answer: Optional[str] = None
    keywords: Optional[str] = None

class FAQResponse(FAQBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
