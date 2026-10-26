import time
import json
from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.conversation import Conversation, Message
from app.models.query_log import QueryLog
from app.schemas.chat import (
    ChatRequest, ChatResponse, ConversationResponse,
    ConversationSummary, SuggestedQuestion, SourceReference
)
from app.core.dependencies import get_current_user, get_optional_current_user
from app.rag.retriever import retriever
from app.rag.gemini_client import gemini_client
from app.rag.fallback_synthesizer import fallback_synthesizer

router = APIRouter(prefix="/chat", tags=["Chatbot"])

@router.post("/message", response_model=ChatResponse)
def send_chat_message(
    payload: ChatRequest,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    start_time = time.time()
    query_text = payload.message.strip()

    if not query_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty."
        )

    # 1. Manage Conversation
    user_id = current_user.id if current_user else None
    conversation = None

    if payload.conversation_id:
        conversation = db.query(Conversation).filter(
            Conversation.id == payload.conversation_id
        ).first()

    if not conversation:
        # Generate initial title from query
        words = query_text.split()
        title = " ".join(words[:6]) if words else "New Chat"
        if len(title) > 40:
            title = title[:40] + "..."
        conversation = Conversation(
            user_id=user_id,
            title=title
        )
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

    # 2. Save User Message
    user_msg = Message(
        conversation_id=conversation.id,
        sender="user",
        content=query_text
    )
    db.add(user_msg)
    db.commit()

    # 3. Retrieve relevant knowledge chunks
    retrieved_items = retriever.search(db=db, query=query_text, top_k=4)

    # Prepare conversation history for context
    past_messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation.id)
        .order_by(Message.timestamp.desc())
        .limit(6)
        .all()
    )
    history = [{"sender": m.sender, "content": m.content} for m in reversed(past_messages)]

    # 4. Generate Response (Gemini API or Fallback Synthesizer)
    bot_content = None
    fallback_triggered = False
    suggested_followups = []
    user_display_name = current_user.name if current_user else "Student"

    # Try Gemini if key is active
    if gemini_client.is_available():
        bot_content = gemini_client.generate_grounded_response(
            query=query_text,
            retrieved_contexts=retrieved_items,
            conversation_history=history
        )

    # If Gemini not active or offline or returned None, use local RAG synthesizer
    if not bot_content:
        synth_result = fallback_synthesizer.synthesize(
            query=query_text,
            retrieved_contexts=retrieved_items,
            user_name=user_display_name
        )
        bot_content = synth_result["content"]
        fallback_triggered = synth_result["fallback_triggered"]
        suggested_followups = synth_result.get("suggested_followups", [])
    else:
        # Check if Gemini output signals an unsupported question
        if "I don't have verified records" in bot_content or "consult the" in bot_content.lower():
            fallback_triggered = True
        suggested_followups = [
            "What are the undergraduate eligibility criteria?",
            "What is the minimum attendance requirement?",
            "What are the semester tuition fees?",
            "Who do I contact at the Registrar's Office?"
        ]

    # Format Source References
    sources = []
    for item in retrieved_items:
        sources.append(
            SourceReference(
                type=item.get("type", "faq"),
                title=item.get("title", "University Resource"),
                category=item.get("category", "General"),
                similarity=item.get("similarity"),
                reference_id=item.get("id")
            )
        )

    # Calculate confidence
    top_score = retrieved_items[0]["similarity"] if retrieved_items else 0.0

    # 5. Save Bot Message
    sources_serialized = json.dumps([s.model_dump() for s in sources]) if sources else None
    bot_msg = Message(
        conversation_id=conversation.id,
        sender="bot",
        content=bot_content,
        sources_json=sources_serialized,
        confidence_score=float(top_score)
    )
    db.add(bot_msg)
    conversation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(bot_msg)

    # 6. Analytics Logging
    elapsed_ms = int((time.time() - start_time) * 1000)
    detected_cat = retrieved_items[0].get("category") if retrieved_items else "Uncategorized"
    
    query_log = QueryLog(
        user_id=user_id,
        query_text=query_text[:500],
        detected_category=detected_cat,
        answered=not fallback_triggered,
        fallback_triggered=fallback_triggered,
        similarity_score=float(top_score),
        response_time_ms=elapsed_ms
    )
    db.add(query_log)
    db.commit()

    return ChatResponse(
        conversation_id=conversation.id,
        message_id=bot_msg.id,
        sender="bot",
        content=bot_content,
        sources=sources,
        fallback_triggered=fallback_triggered,
        suggested_followups=suggested_followups,
        timestamp=bot_msg.timestamp
    )

@router.get("/conversations", response_model=List[ConversationSummary])
def get_user_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conversations = (
        db.query(Conversation)
        .filter(Conversation.user_id == current_user.id)
        .order_by(Conversation.updated_at.desc())
        .all()
    )
    results = []
    for c in conversations:
        results.append(
            ConversationSummary(
                id=c.id,
                title=c.title,
                created_at=c.created_at,
                updated_at=c.updated_at,
                message_count=len(c.messages)
            )
        )
    return results

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
def get_conversation_details(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id)
        .first()
    )
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    return conv

@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_conversation(
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv = (
        db.query(Conversation)
        .filter(Conversation.id == conversation_id, Conversation.user_id == current_user.id)
        .first()
    )
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found.")
    db.delete(conv)
    db.commit()
    return None

@router.delete("/conversations", status_code=status.HTTP_204_NO_CONTENT)
def clear_all_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db.query(Conversation).filter(Conversation.user_id == current_user.id).delete()
    db.commit()
    return None

@router.get("/suggested", response_model=List[SuggestedQuestion])
def get_suggested_questions():
    return [
        SuggestedQuestion(category="Admissions", question="What are the undergraduate eligibility criteria?"),
        SuggestedQuestion(category="Admissions", question="What is the application deadline for 2026-2027?"),
        SuggestedQuestion(category="Examinations", question="How is SGPA and CGPA calculated under CBCS?"),
        SuggestedQuestion(category="Examinations", question="What is the policy for exam revaluation?"),
        SuggestedQuestion(category="Fees", question="What is the semester tuition fee structure?"),
        SuggestedQuestion(category="Fees", question="What is the fee refund policy if a student withdraws?"),
        SuggestedQuestion(category="Scholarships", question="What merit scholarships does the university offer?"),
        SuggestedQuestion(category="Scholarships", question="How can students apply for Need-Based Financial Aid?"),
        SuggestedQuestion(category="Attendance", question="What is the minimum mandatory attendance requirement?"),
        SuggestedQuestion(category="Campus", question="What are the Central Library timings and book rules?"),
        SuggestedQuestion(category="Campus", question="What are the hostel curfew and mess timings?"),
        SuggestedQuestion(category="General", question="How can I contact the Registrar's Office?")
    ]
