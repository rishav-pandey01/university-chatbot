import os
from typing import List, Dict, Any, Optional
from app.config import settings

class GeminiRAGClient:
    def __init__(self):
        self._init_client()

    def _init_client(self):
        self.api_key = (settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY", "")).strip()
        self.client = None
        if self.api_key:
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key)
                print("[Gemini] Client initialized successfully.")
            except Exception as e:
                print(f"[Gemini Warning] Failed to initialize client: {e}")
                self.client = None

    def is_available(self) -> bool:
        if not self.client and (settings.GEMINI_API_KEY or os.getenv("GEMINI_API_KEY")):
            self._init_client()
        return self.client is not None

    def generate_grounded_response(
        self,
        query: str,
        retrieved_contexts: List[Dict[str, Any]],
        conversation_history: Optional[List[Dict[str, str]]] = None
    ) -> Optional[str]:
        """
        Generates a grounded response using Gemini with strict university grounding.
        """
        if not self.is_available():
            return None

        # Build context snippet
        context_text = ""
        for i, item in enumerate(retrieved_contexts):
            source_type = "FAQ" if item.get("type") == "faq" else "Document"
            context_text += f"\n--- Source {i+1} [{source_type}: {item.get('title')}] ---\n{item.get('content')}\n"

        # Conversation history formatted
        history_text = ""
        if conversation_history:
            for msg in conversation_history[-4:]: # Last 4 turns
                role = "Student" if msg.get("sender") == "user" else "CampusBot"
                history_text += f"{role}: {msg.get('content')}\n"

        prompt = f"""You are CampusBot, the official AI-Powered University Student Support Assistant.
Your mission is to provide accurate, professional, empathetic, and context-aware responses to university students.

VERIFIED UNIVERSITY CONTEXT:
{context_text if context_text else "No relevant university knowledge base items found."}

CONVERSATION HISTORY:
{history_text if history_text else "No prior history."}

STUDENT'S QUESTION:
{query}

STRICT GROUNDING GUIDELINES:
1. Base all university policies, fees, deadlines, minimum attendance requirements, exam schedules, and grading calculations strictly on the VERIFIED UNIVERSITY CONTEXT.
2. If the context does not contain sufficient details to answer authoritatively, do NOT guess or fabricate policies, dates, or fee amounts. Politely advise the student to contact the respective university office (e.g. Office of the Registrar: registrar@university.edu, Finance Office, or Academic Cell).
3. If this is a casual greeting (such as 'hello', 'hi', 'good morning'), respond warmly, introduce yourself, and offer suggested topics like Admissions, Fees, Exams, or Scholarships.
4. Structure your response clearly using markdown with bullet points or numbered lists where appropriate.
5. Reference the consulted source titles at the conclusion of your response.
"""
        models_to_try = [
            settings.GEMINI_MODEL,
            "gemini-2.5-flash",
            "gemini-1.5-flash",
            "gemini-2.0-flash",
        ]
        # Remove duplicates while preserving order
        seen = set()
        unique_models = [m for m in models_to_try if m and not (m in seen or seen.add(m))]

        for model_name in unique_models:
            try:
                response = self.client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                if response and response.text:
                    return response.text
            except Exception as e:
                print(f"[Gemini API Notice] Model '{model_name}' failed: {e}. Trying fallback if available...")

        print("[Gemini API Warning] All Gemini models failed or quota exceeded. Using local RAG synthesizer.")
        return None

gemini_client = GeminiRAGClient()
