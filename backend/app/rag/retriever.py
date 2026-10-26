from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

from app.models.faq import FAQ
from app.models.document import Document, DocumentChunk
from app.config import settings

class KnowledgeRetriever:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            ngram_range=(1, 2),
            stop_words="english",
            sublinear_tf=True
        )

    def search(
        self,
        db: Session,
        query: str,
        top_k: int = 4,
        min_threshold: float = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieves top relevant knowledge items (FAQs and Document Chunks) matching the query.
        """
        if min_threshold is None:
            min_threshold = settings.SIMILARITY_THRESHOLD

        cleaned_query = query.strip()
        if not cleaned_query:
            return []

        # 1. Fetch all FAQs and Document Chunks
        faqs = db.query(FAQ).all()
        doc_chunks = db.query(DocumentChunk).join(Document).all()

        items = []
        corpus = []

        # Prepare FAQ items
        for faq in faqs:
            # Combine question, answer, keywords for rich indexing
            text = f"{faq.question} {faq.keywords or ''} {faq.answer}"
            corpus.append(text)
            items.append({
                "type": "faq",
                "id": faq.id,
                "title": faq.question,
                "category": faq.category,
                "content": faq.answer,
                "raw_question": faq.question
            })

        # Prepare Document Chunk items
        for chunk in doc_chunks:
            doc_title = chunk.document.title if chunk.document else "Document"
            doc_cat = chunk.document.category if chunk.document else "General"
            text = f"{doc_title} {doc_cat} {chunk.content}"
            corpus.append(text)
            items.append({
                "type": "document",
                "id": chunk.id,
                "title": f"{doc_title} (Page {chunk.page_number or 1})",
                "category": doc_cat,
                "content": chunk.content,
                "document_id": chunk.document_id
            })

        if not items:
            return []

        try:
            # Fit and transform
            all_texts = [cleaned_query] + corpus
            tfidf_matrix = self.vectorizer.fit_transform(all_texts)
            query_vector = tfidf_matrix[0:1]
            corpus_vectors = tfidf_matrix[1:]

            # Compute Cosine Similarities
            similarities = cosine_similarity(query_vector, corpus_vectors)[0]

            # Boost exact keyword matches for university-critical terms
            query_tokens = set(re.findall(r"\w+", cleaned_query.lower()))
            boosted_scores = []
            for i, score in enumerate(similarities):
                item = items[i]
                item_tokens = set(re.findall(r"\w+", (item["title"] + " " + item.get("category", "")).lower()))
                overlap = len(query_tokens.intersection(item_tokens))
                
                # Bonus if key nouns match in title or category
                boost = 0.08 * overlap
                final_score = float(score) + boost
                boosted_scores.append((final_score, item))

            # Sort by score descending
            boosted_scores.sort(key=lambda x: x[0], reverse=True)

            # Filter results above threshold
            results = []
            for score, item in boosted_scores[:top_k]:
                if score >= min_threshold:
                    results.append({
                        **item,
                        "similarity": round(min(score, 1.0), 3)
                    })

            return results
        except Exception as e:
            # Fallback to simple token matching if vectorization fails
            print(f"Retriever TF-IDF error: {e}")
            return self._keyword_search_fallback(query, items, top_k)

    def _keyword_search_fallback(
        self,
        query: str,
        items: List[Dict[str, Any]],
        top_k: int
    ) -> List[Dict[str, Any]]:
        tokens = set(re.findall(r"\w+", query.lower()))
        if not tokens:
            return []

        scored = []
        for item in items:
            text = f"{item['title']} {item.get('category', '')} {item['content']}".lower()
            matches = sum(1 for t in tokens if t in text)
            if matches > 0:
                score = matches / max(len(tokens), 1)
                scored.append((score, item))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [{**it, "similarity": round(min(sc, 1.0), 3)} for sc, it in scored[:top_k]]

retriever = KnowledgeRetriever()
