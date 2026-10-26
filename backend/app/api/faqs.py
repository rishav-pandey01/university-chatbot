from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.database import get_db
from app.models.faq import FAQ
from app.models.user import User
from app.schemas.faq import FAQCreate, FAQUpdate, FAQResponse
from app.core.dependencies import get_current_active_admin

router = APIRouter(prefix="/faqs", tags=["Knowledge Base FAQs"])

@router.get("", response_model=List[FAQResponse])
def get_faqs(
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(FAQ)
    if category and category.lower() != "all":
        query = query.filter(FAQ.category.ilike(f"%{category}%"))
    if search:
        s = f"%{search.strip()}%"
        query = query.filter((FAQ.question.ilike(s)) | (FAQ.answer.ilike(s)) | (FAQ.keywords.ilike(s)))
    return query.order_by(FAQ.category, FAQ.id).all()

@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(FAQ.category).distinct().all()
    return sorted([c[0] for c in categories if c[0]])

@router.get("/{faq_id}", response_model=FAQResponse)
def get_faq_by_id(faq_id: int, db: Session = Depends(get_db)):
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found.")
    return faq

@router.post("", response_model=FAQResponse, status_code=status.HTTP_201_CREATED)
def create_faq(
    payload: FAQCreate,
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    new_faq = FAQ(
        category=payload.category.strip(),
        question=payload.question.strip(),
        answer=payload.answer.strip(),
        keywords=payload.keywords.strip() if payload.keywords else None
    )
    db.add(new_faq)
    db.commit()
    db.refresh(new_faq)
    return new_faq

@router.put("/{faq_id}", response_model=FAQResponse)
def update_faq(
    faq_id: int,
    payload: FAQUpdate,
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found.")

    if payload.category is not None:
        faq.category = payload.category.strip()
    if payload.question is not None:
        faq.question = payload.question.strip()
    if payload.answer is not None:
        faq.answer = payload.answer.strip()
    if payload.keywords is not None:
        faq.keywords = payload.keywords.strip()

    db.commit()
    db.refresh(faq)
    return faq

@router.delete("/{faq_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_faq(
    faq_id: int,
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    faq = db.query(FAQ).filter(FAQ.id == faq_id).first()
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found.")
    db.delete(faq)
    db.commit()
    return None
