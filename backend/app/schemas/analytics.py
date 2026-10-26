from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Optional

class CategoryCount(BaseModel):
    category: str
    count: int

class DashboardStatsResponse(BaseModel):
    total_users: int
    total_conversations: int
    total_queries: int
    total_faqs: int
    total_documents: int
    feedback_helpful_count: int
    feedback_unhelpful_count: int
    satisfaction_rate: float
    fallback_rate: float
    category_distribution: List[CategoryCount] = []

class UnansweredQueryResponse(BaseModel):
    id: int
    query_text: str
    detected_category: Optional[str] = None
    similarity_score: Optional[float] = None
    resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ResolveQueryRequest(BaseModel):
    resolved: bool = True
