import os
from typing import List, Dict, Any
from pypdf import PdfReader

def extract_text_from_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Extracts text from a file (PDF or TXT) and returns a list of pages/chunks with metadata.
    """
    ext = os.path.splitext(file_path)[1].lower()
    pages_data = []

    if ext == ".pdf":
        reader = PdfReader(file_path)
        for idx, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            text = text.strip()
            if text:
                pages_data.append({
                    "page_number": idx + 1,
                    "text": text
                })
    elif ext in [".txt", ".md", ".csv"]:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read().strip()
            if content:
                pages_data.append({
                    "page_number": 1,
                    "text": content
                })
    return pages_data

def chunk_text(text: str, chunk_size: int = 600, overlap: int = 100) -> List[str]:
    """
    Splits text into overlapping chunks, attempting to split on paragraph or sentence boundaries.
    """
    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        if end >= len(text):
            chunks.append(text[start:].strip())
            break

        # Look for a paragraph break or period near the end
        break_pos = text.rfind("\n\n", start, end)
        if break_pos == -1 or break_pos < start + (chunk_size // 2):
            break_pos = text.rfind(".\n", start, end)
        if break_pos == -1 or break_pos < start + (chunk_size // 2):
            break_pos = text.rfind(". ", start, end)
        if break_pos == -1 or break_pos < start + (chunk_size // 2):
            break_pos = end

        chunk = text[start:break_pos + 1].strip()
        if chunk:
            chunks.append(chunk)

        start = max(start + 1, break_pos + 1 - overlap)

    return [c for c in chunks if len(c) > 30]
