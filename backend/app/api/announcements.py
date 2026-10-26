from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.announcement import Announcement
from app.models.user import User
from app.schemas.announcement import AnnouncementCreate, AnnouncementUpdate, AnnouncementResponse
from app.core.dependencies import get_current_active_admin

router = APIRouter(prefix="/announcements", tags=["Announcements"])

@router.get("", response_model=List[AnnouncementResponse])
def get_announcements(db: Session = Depends(get_db)):
    return (
        db.query(Announcement)
        .filter(Announcement.is_active == True)
        .order_by(Announcement.priority.desc(), Announcement.created_at.desc())
        .all()
    )

@router.get("/all", response_model=List[AnnouncementResponse])
def get_all_announcements_admin(
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    return db.query(Announcement).order_by(Announcement.created_at.desc()).all()

@router.post("", response_model=AnnouncementResponse, status_code=status.HTTP_201_CREATED)
def create_announcement(
    payload: AnnouncementCreate,
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    ann = Announcement(
        title=payload.title.strip(),
        content=payload.content.strip(),
        category=payload.category.strip(),
        priority=payload.priority.strip(),
        is_active=payload.is_active
    )
    db.add(ann)
    db.commit()
    db.refresh(ann)
    return ann

@router.put("/{announcement_id}", response_model=AnnouncementResponse)
def update_announcement(
    announcement_id: int,
    payload: AnnouncementUpdate,
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    ann = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found.")

    if payload.title is not None:
        ann.title = payload.title.strip()
    if payload.content is not None:
        ann.content = payload.content.strip()
    if payload.category is not None:
        ann.category = payload.category.strip()
    if payload.priority is not None:
        ann.priority = payload.priority.strip()
    if payload.is_active is not None:
        ann.is_active = payload.is_active

    db.commit()
    db.refresh(ann)
    return ann

@router.delete("/{announcement_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_announcement(
    announcement_id: int,
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    ann = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not ann:
        raise HTTPException(status_code=404, detail="Announcement not found.")
    db.delete(ann)
    db.commit()
    return None
