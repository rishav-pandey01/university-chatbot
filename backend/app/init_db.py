import os
from sqlalchemy.orm import Session
from app.database import engine, Base, SessionLocal
from app.models.user import User
from app.models.faq import FAQ
from app.models.announcement import Announcement
from app.models.document import Document, DocumentChunk
from app.core.security import hash_password
from app.rag.seed_data import SAMPLE_FAQS, SAMPLE_ANNOUNCEMENTS, SAMPLE_DOCUMENT
from app.rag.text_extractor import chunk_text
from app.config import settings

def init_database():
    """
    Initializes database tables and populates default demo data if empty.
    """
    # Create all tables
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # 1. Seed Default Admin User
        admin_user = db.query(User).filter(User.email == "admin@university.edu").first()
        if not admin_user:
            admin_user = User(
                name="University Administrator",
                email="admin@university.edu",
                password_hash=hash_password("Admin@123"),
                role="admin"
            )
            db.add(admin_user)

        # 2. Seed Default Student User
        student_user = db.query(User).filter(User.email == "student@university.edu").first()
        if not student_user:
            student_user = User(
                name="Alex Sharma",
                email="student@university.edu",
                password_hash=hash_password("Student@123"),
                role="student"
            )
            db.add(student_user)

        # 3. Seed FAQs if empty
        faq_count = db.query(FAQ).count()
        if faq_count == 0:
            for faq_data in SAMPLE_FAQS:
                faq = FAQ(
                    category=faq_data["category"],
                    question=faq_data["question"],
                    answer=faq_data["answer"],
                    keywords=faq_data.get("keywords")
                )
                db.add(faq)

        # 4. Seed Announcements if empty
        ann_count = db.query(Announcement).count()
        if ann_count == 0:
            for ann_data in SAMPLE_ANNOUNCEMENTS:
                ann = Announcement(
                    title=ann_data["title"],
                    content=ann_data["content"],
                    category=ann_data.get("category", "General"),
                    priority=ann_data.get("priority", "normal"),
                    is_active=True
                )
                db.add(ann)

        # 5. Seed Official Document if empty
        doc_count = db.query(Document).count()
        if doc_count == 0:
            os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
            doc_file_path = os.path.join(settings.UPLOAD_DIR, SAMPLE_DOCUMENT["filename"])
            with open(doc_file_path, "w", encoding="utf-8") as f:
                f.write(SAMPLE_DOCUMENT["content"])

            doc = Document(
                title=SAMPLE_DOCUMENT["title"],
                filename=SAMPLE_DOCUMENT["filename"],
                file_path=doc_file_path,
                category=SAMPLE_DOCUMENT["category"],
                file_size_kb=len(SAMPLE_DOCUMENT["content"]) // 1024 + 1
            )
            db.add(doc)
            db.commit()
            db.refresh(doc)

            # Chunk document
            chunks = chunk_text(SAMPLE_DOCUMENT["content"], chunk_size=500, overlap=80)
            for i, c in enumerate(chunks):
                chunk = DocumentChunk(
                    document_id=doc.id,
                    chunk_index=i,
                    content=c,
                    page_number=1
                )
                db.add(chunk)

        db.commit()
        print("Database initialized and seeded successfully.")
    except Exception as e:
        db.rollback()
        print(f"Error during database initialization: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
