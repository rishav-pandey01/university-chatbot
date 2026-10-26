import re
from typing import List, Dict, Any, Tuple

class FallbackSynthesizer:
    GREETING_PATTERNS = [
        r"^(hi|hello|hey|greetings|good morning|good afternoon|good evening|howdy)\b",
        r"^(who are you|what can you do|help me|what is campusbot)\b"
    ]

    DEPT_DIRECTORY = {
        "Admissions": "Office of Admissions (Email: admissions@university.edu | Ext: 101)",
        "Examinations": "Controller of Examinations (Email: examcell@university.edu | Ext: 202)",
        "Fees": "Finance & Accounts Office (Email: accounts@university.edu | Ext: 303)",
        "Scholarships": "Student Welfare & Scholarship Cell (Email: scholarships@university.edu | Ext: 404)",
        "Attendance": "Dean of Academic Affairs (Email: academic.section@university.edu | Ext: 505)",
        "Campus": "Campus Facilities & Hostel Warden (Email: campuslife@university.edu | Ext: 606)",
        "General": "Registrar's Office (Email: registrar@university.edu | Ext: 100)"
    }

    def is_greeting(self, query: str) -> bool:
        normalized = query.lower().strip()
        for pattern in self.GREETING_PATTERNS:
            if re.search(pattern, normalized):
                return True
        return False

    def handle_greeting(self, user_name: str = "Student") -> Dict[str, Any]:
        return {
            "content": f"Hello {user_name}! 👋 Welcome to the **University Student Support Assistant**.\n\n"
                       f"I can assist you with:\n"
                       f"- 🎓 **Admissions & Eligibility**\n"
                       f"- 📝 **Examination Schedules & Grading**\n"
                       f"- 💳 **Tuition Fees & Payment Options**\n"
                       f"- 🏅 **Merit & Need-Based Scholarships**\n"
                       f"- 📋 **Attendance Regulations (75% rule)**\n"
                       f"- 🏫 **Hostel, Library & Campus Facilities**\n\n"
                       f"How may I help you today? You can select a suggested topic below or type your question.",
            "fallback_triggered": False,
            "suggested_followups": [
                "What is the minimum attendance requirement?",
                "How is SGPA and CGPA calculated?",
                "What are the semester tuition fees?",
                "How do I apply for merit scholarships?"
            ]
        }

    def synthesize(
        self,
        query: str,
        retrieved_contexts: List[Dict[str, Any]],
        user_name: str = "Student"
    ) -> Dict[str, Any]:
        """
        Synthesizes an intelligent, structured response grounded in verified retrieved chunks.
        """
        # 1. Check greeting
        if self.is_greeting(query) and len(query.split()) <= 4:
            return self.handle_greeting(user_name)

        # 2. Check if we found relevant verified knowledge
        if not retrieved_contexts:
            # Fallback when no reliable knowledge is available
            return self._build_fallback_response(query)

        # 3. Best match content
        top_match = retrieved_contexts[0]
        category = top_match.get("category", "General")
        
        # Format response
        response_lines = []
        
        # If top match is an FAQ
        if top_match.get("type") == "faq":
            response_lines.append(f"### {top_match.get('title')}")
            response_lines.append(f"\n{top_match.get('content')}\n")
        else:
            response_lines.append(f"### Verified Policy: {top_match.get('title')}")
            response_lines.append(f"\n{top_match.get('content')}\n")

        # Additional supporting context if available
        if len(retrieved_contexts) > 1:
            secondary = retrieved_contexts[1]
            if secondary.get("similarity", 0) >= 0.35 and secondary.get("title") != top_match.get("title"):
                response_lines.append(f"\n**Related Information ({secondary.get('title')}):**")
                snippet = secondary.get('content')
                if len(snippet) > 280:
                    snippet = snippet[:280] + "..."
                response_lines.append(f"{snippet}\n")

        # Add official source reference
        response_lines.append(f"\n---")
        response_lines.append(f"📚 **Verified Source:** {top_match.get('title')} ({category} Section)")
        
        # Department contact
        dept_info = self.DEPT_DIRECTORY.get(category, self.DEPT_DIRECTORY["General"])
        response_lines.append(f"📞 **Need further assistance?** Contact {dept_info}.")

        # Generate follow-up suggestions based on category
        followups = self._get_followups_for_category(category)

        return {
            "content": "\n".join(response_lines),
            "fallback_triggered": False,
            "suggested_followups": followups
        }

    def _build_fallback_response(self, query: str) -> Dict[str, Any]:
        """
        Constructs a polite, clear fallback response when information is not in knowledge base.
        """
        # Try to infer category
        inferred_category = "General"
        q_lower = query.lower()
        if any(w in q_lower for w in ["admission", "apply", "eligibility", "entrance"]):
            inferred_category = "Admissions"
        elif any(w in q_lower for w in ["exam", "grade", "gpa", "cgpa", "marks", "result", "backlog"]):
            inferred_category = "Examinations"
        elif any(w in q_lower for w in ["fee", "payment", "tuition", "challan", "refund"]):
            inferred_category = "Fees"
        elif any(w in q_lower for w in ["scholarship", "financial aid", "waiver", "stipend"]):
            inferred_category = "Scholarships"
        elif any(w in q_lower for w in ["attendance", "leave", "medical", "absent", "shortage"]):
            inferred_category = "Attendance"
        elif any(w in q_lower for w in ["hostel", "library", "wifi", "mess", "hospital", "sports"]):
            inferred_category = "Campus"

        dept = self.DEPT_DIRECTORY.get(inferred_category, self.DEPT_DIRECTORY["General"])

        return {
            "content": (
                f"I couldn't find a verified university policy matching your exact question: *\"{query}\"*.\n\n"
                f"To ensure you receive accurate and up-to-date guidance without misinformation, please consult:\n\n"
                f"🏛️ **{dept}**\n\n"
                f"You can also check the University Student ERP portal or speak directly with your Academic Faculty Mentor."
            ),
            "fallback_triggered": True,
            "suggested_followups": [
                "What is the minimum attendance requirement?",
                "What are the undergraduate eligibility criteria?",
                "What are the semester tuition fees?",
                "Who do I contact at the Registrar's Office?"
            ]
        }

    def _get_followups_for_category(self, category: str) -> List[str]:
        mapping = {
            "Admissions": [
                "What is the application deadline for 2026-2027?",
                "What documents are required during admission verification?",
                "Are international students eligible for admission?"
            ],
            "Examinations": [
                "How is SGPA and CGPA calculated?",
                "What is the policy for exam revaluation?",
                "What are the rules regarding backlog examinations?"
            ],
            "Fees": [
                "What payment methods and installments are supported?",
                "What is the fee refund policy if I withdraw?",
                "What are the hostel and mess charges?"
            ],
            "Scholarships": [
                "What merit scholarships are offered?",
                "How can I apply for Need-Based Financial Aid?",
                "Does the university facilitate government scholarships (NSP)?"
            ],
            "Attendance": [
                "What is the procedure for submitting medical leave?",
                "What happens if attendance falls below 65%?",
                "What are the condonation rules?"
            ],
            "Campus": [
                "What are the Central Library timings and book rules?",
                "What are the hostel facilities and mess timings?",
                "How do students connect to campus Wi-Fi?"
            ],
            "General": [
                "How can I contact the Registrar's Office?",
                "How do I obtain a Bonafide Certificate?",
                "What are the campus emergency contact numbers?"
            ]
        }
        return mapping.get(category, mapping["General"])

fallback_synthesizer = FallbackSynthesizer()
