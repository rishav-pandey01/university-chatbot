from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.feedback import Feedback
from app.models.conversation import Message
from app.models.user import User
from app.schemas.feedback import FeedbackCreate, FeedbackResponse
from app.core.dependencies import get_optional_current_user, get_current_active_admin

router = APIRouter(prefix="/feedback", tags=["Chatbot Feedback"])

@router.post("", response_model=FeedbackResponse, status_code=status.HTTP_201_CREATED)
def submit_feedback(
    payload: FeedbackCreate,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    msg = db.query(Message).filter(Message.id == payload.message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found.")

    fb = Feedback(
        message_id=payload.message_id,
        user_id=current_user.id if current_user else None,
        rating=payload.rating.strip().lower(),
        comment=payload.comment.strip() if payload.comment else None
    )
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb

@router.get("", response_model=List[FeedbackResponse])
def get_all_feedback(
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    return db.query(Feedback).order_by(Feedback.created_at.desc()).limit(100).all()
