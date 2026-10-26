from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.database import get_db
from app.models.user import User
from app.models.conversation import Conversation
from app.models.faq import FAQ
from app.models.document import Document
from app.models.feedback import Feedback
from app.models.query_log import QueryLog
from app.schemas.analytics import DashboardStatsResponse, UnansweredQueryResponse, ResolveQueryRequest, CategoryCount
from app.core.dependencies import get_current_active_admin

router = APIRouter(prefix="/analytics", tags=["Admin Analytics"])

@router.get("/dashboard", response_model=DashboardStatsResponse)
def get_dashboard_metrics(
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    total_users = db.query(func.count(User.id)).scalar() or 0
    total_conversations = db.query(func.count(Conversation.id)).scalar() or 0
    total_queries = db.query(func.count(QueryLog.id)).scalar() or 0
    total_faqs = db.query(func.count(FAQ.id)).scalar() or 0
    total_docs = db.query(func.count(Document.id)).scalar() or 0

    helpful = db.query(func.count(Feedback.id)).filter(Feedback.rating == "helpful").scalar() or 0
    unhelpful = db.query(func.count(Feedback.id)).filter(Feedback.rating == "unhelpful").scalar() or 0
    total_fb = helpful + unhelpful
    satisfaction_rate = round((helpful / total_fb) * 100, 1) if total_fb > 0 else 100.0

    fallback_count = db.query(func.count(QueryLog.id)).filter(QueryLog.fallback_triggered == True).scalar() or 0
    fallback_rate = round((fallback_count / total_queries) * 100, 1) if total_queries > 0 else 0.0

    # Category distribution
    cat_rows = (
        db.query(QueryLog.detected_category, func.count(QueryLog.id))
        .filter(QueryLog.detected_category.isnot(None))
        .group_by(QueryLog.detected_category)
        .all()
    )
    cat_distribution = [CategoryCount(category=c[0] or "General", count=c[1]) for c in cat_rows]

    return DashboardStatsResponse(
        total_users=total_users,
        total_conversations=total_conversations,
        total_queries=total_queries,
        total_faqs=total_faqs,
        total_documents=total_docs,
        feedback_helpful_count=helpful,
        feedback_unhelpful_count=unhelpful,
        satisfaction_rate=satisfaction_rate,
        fallback_rate=fallback_rate,
        category_distribution=cat_distribution
    )

@router.get("/unanswered", response_model=List[UnansweredQueryResponse])
def get_unanswered_queries(
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    logs = (
        db.query(QueryLog)
        .filter((QueryLog.fallback_triggered == True) | (QueryLog.answered == False))
        .order_by(QueryLog.created_at.desc())
        .limit(100)
        .all()
    )
    return logs

@router.put("/unanswered/{log_id}/resolve", response_model=UnansweredQueryResponse)
def resolve_unanswered_query(
    log_id: int,
    payload: ResolveQueryRequest,
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    log = db.query(QueryLog).filter(QueryLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Query log not found.")
    log.resolved = payload.resolved
    db.commit()
    db.refresh(log)
    return log
