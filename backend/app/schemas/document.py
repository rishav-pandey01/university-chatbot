from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class DocumentChunkResponse(BaseModel):
    id: int
    chunk_index: int
    content: str
    page_number: Optional[int] = None

    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: int
    title: str
    filename: str
    category: str
    file_size_kb: int
    uploaded_at: datetime
    chunk_count: int = 0

    class Config:
        from_attributes = True
