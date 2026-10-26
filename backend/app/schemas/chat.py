from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Any

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[int] = None

class SourceReference(BaseModel):
    type: str # "faq" or "document"
    title: str
    category: Optional[str] = None
    similarity: Optional[float] = None
    reference_id: Optional[int] = None

class ChatResponse(BaseModel):
    conversation_id: int
    message_id: int
    sender: str
    content: str
    sources: List[SourceReference] = []
    fallback_triggered: bool = False
    suggested_followups: List[str] = []
    timestamp: datetime

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender: str
    content: str
    sources_json: Optional[str] = None
    confidence_score: Optional[float] = None
    timestamp: datetime

    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []

    class Config:
        from_attributes = True

class ConversationSummary(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0

class SuggestedQuestion(BaseModel):
    category: str
    question: str
