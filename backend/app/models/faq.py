from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from app.database import Base

class FAQ(Base):
    __tablename__ = "faqs"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(50), nullable=False, index=True) # Admissions, Exams, Fees, Scholarships, Attendance, Courses, Campus, General
    question = Column(String(300), nullable=False, index=True)
    answer = Column(Text, nullable=False)
    keywords = Column(String(255), nullable=True) # Comma-separated keywords for fast tagging
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
