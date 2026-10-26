from sqlalchemy import Column, Integer, String, Text, Boolean, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class QueryLog(Base):
    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    query_text = Column(String(500), nullable=False)
    detected_category = Column(String(50), nullable=True)
    answered = Column(Boolean, default=True)
    fallback_triggered = Column(Boolean, default=False)
    resolved = Column(Boolean, default=False) # Marked by admin when resolved/added to FAQ
    similarity_score = Column(Float, nullable=True)
    response_time_ms = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
