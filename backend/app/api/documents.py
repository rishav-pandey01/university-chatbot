import os
import shutil
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List, Optional

from app.database import get_db
from app.models.document import Document, DocumentChunk
from app.models.user import User
from app.schemas.document import DocumentResponse
from app.core.dependencies import get_current_active_admin
from app.rag.text_extractor import extract_text_from_file, chunk_text
from app.config import settings

router = APIRouter(prefix="/documents", tags=["Knowledge Base Documents"])

@router.get("", response_model=List[DocumentResponse])
def get_documents(db: Session = Depends(get_db)):
    docs = db.query(Document).order_by(Document.uploaded_at.desc()).all()
    results = []
    for d in docs:
        results.append(
            DocumentResponse(
                id=d.id,
                title=d.title,
                filename=d.filename,
                category=d.category,
                file_size_kb=d.file_size_kb,
                uploaded_at=d.uploaded_at,
                chunk_count=len(d.chunks)
            )
        )
    return results

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    category: str = Form("General"),
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    # Validate extension
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    if ext not in [".pdf", ".txt", ".md"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file format. Please upload a PDF or TXT document."
        )

    # Save to disk
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    safe_filename = f"{int(os.times().elapsed * 1000)}_{filename.replace(' ', '_')}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size_kb = int(os.path.getsize(file_path) / 1024)

    # Create Document record
    new_doc = Document(
        title=title.strip(),
        filename=filename,
        file_path=file_path,
        category=category.strip(),
        file_size_kb=file_size_kb
    )
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # Extract text and chunk
    try:
        pages = extract_text_from_file(file_path)
        chunk_idx = 0
        for page in pages:
            raw_text = page["text"]
            page_num = page["page_number"]
            chunks = chunk_text(raw_text)
            for c in chunks:
                doc_chunk = DocumentChunk(
                    document_id=new_doc.id,
                    chunk_index=chunk_idx,
                    content=c,
                    page_number=page_num
                )
                db.add(doc_chunk)
                chunk_idx += 1
        db.commit()
        db.refresh(new_doc)
    except Exception as e:
        print(f"Error extracting/chunking document: {e}")

    return DocumentResponse(
        id=new_doc.id,
        title=new_doc.title,
        filename=new_doc.filename,
        category=new_doc.category,
        file_size_kb=new_doc.file_size_kb,
        uploaded_at=new_doc.uploaded_at,
        chunk_count=len(new_doc.chunks)
    )

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(
    document_id: int,
    current_admin: User = Depends(get_current_active_admin),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == document_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    # Remove physical file
    if os.path.exists(doc.file_path):
        try:
            os.remove(doc.file_path)
        except Exception:
            pass

    db.delete(doc)
    db.commit()
    return None
