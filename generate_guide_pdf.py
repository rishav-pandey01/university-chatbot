import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "UniBot: AI-Powered University Student Support System — Presentation & Defense Guide")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 742, letter[0] - 54, 742)

        # Footer
        footer_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 34, footer_text)
        self.drawString(54, 34, "Confidential — Prepared for Academic Project Defense & Evaluation")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 46, letter[0] - 54, 46)

        self.restoreState()

def build_pdf(filename="UniBot_Presentation_Defense_Guide.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom Palettes
    navy = colors.HexColor("#1e3a8a")
    blue = colors.HexColor("#2563eb")
    dark_slate = colors.HexColor("#0f172a")
    text_color = colors.HexColor("#334155")
    bg_light = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#cbd5e1")
    accent_green = colors.HexColor("#16a34a")
    accent_amber = colors.HexColor("#b45309")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=navy,
        spaceAfter=6
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=blue,
        spaceAfter=15
    )

    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=navy,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=blue,
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=text_color,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=text_color,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )

    q_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=navy
    )

    simple_ans_style = ParagraphStyle(
        'SimpleAns',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=dark_slate
    )

    tech_ans_style = ParagraphStyle(
        'TechAns',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1e40af")
    )

    tip_style = ParagraphStyle(
        'TipStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=12,
        textColor=accent_amber
    )

    story = []

    # ── HEADER BANNER ──
    story.append(Paragraph("UniBot — Project Defense & Viva Master Guide", title_style))
    story.append(Paragraph("AI-Powered University Student Support System | Architecture, RAG Pipeline & Cross-Questioning Defense", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=2, color=blue, spaceBefore=0, spaceAfter=14))

    # ── SECTION 1: EXECUTIVE PROJECT OVERVIEW ──
    story.append(Paragraph("1. Executive Overview (How to Explain Your Project in 60 Seconds)", h1_style))
    story.append(Paragraph(
        "<b>In Simple Words:</b> UniBot is an intelligent, 24/7 web-based assistant built for university campuses. "
        "Every semester, students struggle with repeated questions about admissions, examination grading, tuition fees, scholarship eligibility, "
        "and campus rules. Administrative offices are flooded with inquiries, leading to long queues and delayed responses.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Solution:</b> UniBot solves this by giving students instant, highly accurate answers grounded in verified university documents. "
        "Unlike generic ChatGPT, UniBot does not hallucinate fake fees or rules because it uses a <b>Retrieval-Augmented Generation (RAG)</b> pipeline. "
        "Additionally, it features a <b>Dual-Engine Architecture</b>: it connects to Google Gemini AI for rich conversational responses, but seamlessly falls back "
        "to a built-in semantic knowledge synthesizer if the internet drops or API quota runs out.",
        body_style
    ))

    # Overview Table
    overview_data = [
        [Paragraph("<b>Component</b>", body_style), Paragraph("<b>Technology Used</b>", body_style), Paragraph("<b>Key Responsibility</b>", body_style)],
        [Paragraph("Frontend UI", body_style), Paragraph("React 19 + Vite + Vanilla CSS", body_style), Paragraph("Responsive student chat, FAQ accordion, notices, admin portal", body_style)],
        [Paragraph("Backend API", body_style), Paragraph("FastAPI (Python 3.13) + Uvicorn", body_style), Paragraph("Asynchronous REST endpoints, JWT auth, RAG orchestration", body_style)],
        [Paragraph("Database", body_style), Paragraph("SQLite + SQLAlchemy ORM", body_style), Paragraph("Stores users, conversations, messages, FAQs, notices, audit logs", body_style)],
        [Paragraph("AI / LLM", body_style), Paragraph("Google GenAI (Gemini 2.5 Flash)", body_style), Paragraph("Context-grounded natural language synthesis with citation linking", body_style)],
        [Paragraph("RAG Engine", body_style), Paragraph("Scikit-Learn (TF-IDF + Cosine)", body_style), Paragraph("Sublinear vector indexing, keyword matching & similarity scoring", body_style)]
    ]
    t = Table(overview_data, colWidths=[90, 160, 254])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#e0e7ff")),
        ('TEXTCOLOR', (0,0), (-1,0), navy),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 12))

    # ── SECTION 2: HOW THE SYSTEM WORKS (THE RAG PIPELINE) ──
    story.append(Paragraph("2. How the RAG Pipeline Works (Step-by-Step)", h1_style))
    story.append(Paragraph(
        "When an evaluator asks: <i>'What happens between the student pressing Send and receiving an answer?'</i>, give this 5-step explanation:",
        body_style
    ))

    rag_steps = [
        "<b>Step 1 — Query Ingestion:</b> The student types a question in React. An authenticated or anonymous request reaches the FastAPI <code>/api/chat/message</code> endpoint.",
        "<b>Step 2 — Semantic Retrieval:</b> The <code>KnowledgeRetriever</code> scans all verified university FAQs and uploaded document text chunks using TF-IDF vectorization and cosine similarity to extract the top 4 most relevant excerpts above a similarity threshold (0.25).",
        "<b>Step 3 — Context Prompt Assembly:</b> The retrieved excerpts, the last 4 messages of conversation history, and strict grounding instructions are assembled into an augmented prompt.",
        "<b>Step 4 — Grounded Synthesis:</b> The prompt is sent to Gemini 2.5 Flash. If Gemini is unavailable, the local <code>fallback_synthesizer</code> uses semantic rule extraction to construct a factual response directly from the retrieved knowledge.",
        "<b>Step 5 — Confidence & Audit:</b> The response is saved to the SQLite database with source citations, similarity score, and latency metrics. The student can submit thumbs up/down feedback."
    ]
    for step in rag_steps:
        story.append(Paragraph(f"• {step}", bullet_style))

    story.append(Spacer(1, 14))

    # ── SECTION 3: PRESENTATION & DEFENSE CROSS-QUESTIONS ──
    story.append(Paragraph("3. Master Defense: Handling All Cross-Questions", h1_style))
    story.append(Paragraph("Study these questions carefully. Each includes a simple conversational answer and a technical justification.", body_style))

    def make_qa_card(q_num, question, simple_ans, tech_ans, presentation_tip=None):
        card_content = [
            [Paragraph(f"<b>Q{q_num}: {question}</b>", q_style)],
            [Paragraph(f"<b>Simple Answer:</b> {simple_ans}", simple_ans_style)],
            [Paragraph(f"<b>Technical Defense:</b> {tech_ans}", tech_ans_style)]
        ]
        if presentation_tip:
            card_content.append([Paragraph(f"💡 <b>Presentation Tip:</b> {presentation_tip}", tip_style)])

        card_table = Table(card_content, colWidths=[504])
        card_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), bg_light),
            ('BOX', (0,0), (-1,-1), 1, border_color),
            ('LINELEFT', (0,0), (0,-1), 3.5, blue),
            ('TOPPADDING', (0,0), (-1,-1), 5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 5),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        return KeepTogether([card_table, Spacer(1, 8)])

    # Group 1: Architecture & Frameworks
    story.append(Paragraph("Category A: Architecture & Engineering Choices", h2_style))

    story.append(make_qa_card(
        1,
        "Why did you choose FastAPI over Flask or Django?",
        "FastAPI is modern, extremely fast, and built specifically for asynchronous APIs. Django is too heavy and monolithic for a dedicated chatbot service, while Flask lacks native asynchronous handling and automatic schema validation.",
        "FastAPI uses Starlette for high async concurrency (ASGI) and Pydantic v2 for data validation. It generates interactive OpenAPI docs automatically at /docs and delivers throughput comparable to NodeJS and Go.",
        "Highlight that universities experience high traffic spikes during exam results or admissions, where async I/O is critical."
    ))

    story.append(make_qa_card(
        2,
        "Why use RAG instead of fine-tuning an LLM?",
        "Fine-tuning a model is expensive, time-consuming, and outdated the moment university fees or deadlines change next semester. RAG allows administrators to upload a new PDF or edit an FAQ, and the bot knows the new rule in 1 second without retraining.",
        "Fine-tuning alters internal model weights without guaranteeing factual recall. RAG decouples knowledge storage from language generation, eliminating retraining costs and enabling real-time knowledge base updates.",
        "Use the phrase: 'RAG gives us a living knowledge base, not a frozen snapshot.'"
    ))

    story.append(make_qa_card(
        3,
        "Why did you build a Dual-Engine architecture (Gemini + Local Synthesizer)?",
        "If the internet connection fails or the university runs out of API budget, most AI chatbots completely break. Our chatbot automatically detects if the external API fails and switches to an internal semantic synthesizer so students always get their answers.",
        "The system wraps external model invocations with a try-catch block and checks gemini_client.is_available(). If generation fails or returns HTTP 429/500, execution falls back seamlessly to the local fallback synthesizer with zero downtime.",
        "Emphasize reliability and fault tolerance — evaluators love systems with built-in disaster recovery."
    ))

    story.append(PageBreak())

    # Group 2: AI, Retrieval & Accuracy
    story.append(Paragraph("Category B: AI, Retrieval & Hallucination Prevention", h2_style))

    story.append(make_qa_card(
        4,
        "How do you prevent hallucinations (bot making up fake numbers or rules)?",
        "We constrain the model with strict system instructions: it is strictly forbidden from guessing. It is instructed to answer ONLY from the verified university context. If the context does not contain the answer, it gives a polite referral to the Registrar's Office.",
        "Grounding is enforced via two layers: prompt boundary injection (STRICT GROUNDING GUIDELINES) and retrieval gating (similarity threshold of 0.25). Furthermore, if similarity is low, fallback_triggered is flagged in the query log for admin review.",
        "Mention that accuracy is far more important than creativity in university policies."
    ))

    story.append(make_qa_card(
        5,
        "Why did you use TF-IDF and Cosine Similarity for the retriever instead of a vector database like Pinecone or Chroma?",
        "TF-IDF is lightweight, instantaneous to compute, runs completely offline, and requires zero external cloud hosting fees or heavy dependencies. For a university knowledge base with hundreds of policy documents, TF-IDF + Cosine Similarity provides sub-millisecond lookups with exact keyword preservation.",
        "We configured TfidfVectorizer with sublinear_tf=True and ngram_range=(1,2) to capture domain bigrams (e.g., 'semester fee', 'passing grade'). We also added an exact keyword boosting heuristic that prioritizes title and category matches.",
        "Add: 'Our retriever architecture is modular — we can swap TF-IDF for ChromaDB or pgvector by simply replacing the retriever class.'"
    ))

    story.append(make_qa_card(
        6,
        "How does the bot maintain conversation history?",
        "When a student asks follow-up questions like 'What about for SC/ST category?', the bot remembers the prior context because we store conversations in the database and feed the last 4 turns into the LLM prompt.",
        "The Message table records sender and content linked to a conversation_id. In chat.py, past messages are ordered by timestamp and passed as structured history to Gemini or the local synthesizer.",
        None
    ))

    # Group 3: Data, Ingestion & Administration
    story.append(Paragraph("Category C: Document Processing & Administration", h2_style))

    story.append(make_qa_card(
        7,
        "How do you process uploaded PDF documents in the admin dashboard?",
        "When an admin uploads a circular or policy handbook PDF, our system extracts the text page-by-page using PyPDF and splits large text into overlapping chunks so the retriever can pinpoint the exact paragraph.",
        "The text extractor uses sliding window chunking (approx 600-800 characters with 100 character overlap). Each DocumentChunk is saved in the database with its document_id and page_number, enabling precise citations.",
        "Mention that students see citations like 'Academic Handbook (Page 4)' in their chat answers."
    ))

    story.append(make_qa_card(
        8,
        "What happens when a student asks something the bot does not know?",
        "The system detects low similarity or fallback activation, answers politely with contact details, and records the question into the Unanswered Queries table. The administrator can view this list on their dashboard and add the missing FAQ with one click.",
        "This forms a continuous feedback loop: student queries highlight knowledge gaps, admins populate new answers, and the system continuously grows smarter without code changes.",
        "Evaluators love this — call it an 'Active Learning / Feedback Loop'."
    ))

    story.append(PageBreak())

    # Group 4: Security, Database & Scalability
    story.append(Paragraph("Category D: Security, Database & Scalability", h2_style))

    story.append(make_qa_card(
        9,
        "How is security and authentication handled?",
        "We use industry-standard JSON Web Tokens (JWT). Passwords are never stored as plain text — they are salted and hashed using bcrypt. Sensitive admin endpoints are protected by role-based guards.",
        "FastAPI dependencies (get_current_user and get_current_active_admin) extract and verify the bearer token signature on protected routes. Unauthorized users receive HTTP 401/403 errors.",
        "Confirm that guest students can still chat without logging in, reducing friction for quick inquiries."
    ))

    story.append(make_qa_card(
        10,
        "Why SQLite? Can this scale to thousands of students?",
        "SQLite was chosen for local development and self-contained zero-configuration portability. However, because we use SQLAlchemy ORM, switching to PostgreSQL or MySQL in production requires changing just ONE line in .env (DATABASE_URL) without rewriting any queries.",
        "SQLAlchemy abstracts all DDL and queries. In a production deployment with Docker and Kubernetes, the backend connects to an enterprise PostgreSQL cluster with connection pooling.",
        "State clearly: 'SQLite is our development driver; the code is 100% database agnostic.'"
    ))

    story.append(make_qa_card(
        11,
        "How did you prevent API keys from leaking to GitHub?",
        "All secrets, tokens, and database files are isolated in .env and .gitignore. When we initialized and pushed the repository, git was verified to stage only clean source code. The repository contains a sanitized .env.example template for new developers.",
        "We implemented comprehensive .gitignore rules covering **/.env, *.db, .venv/, and node_modules/.",
        None
    ))

    # ── SECTION 4: PRESENTATION CHECKLIST ──
    story.append(Spacer(1, 6))
    story.append(Paragraph("4. Quick Presentation Checklist & Demo Flow", h1_style))

    checklist_items = [
        "<b>1. Introduce the Problem:</b> State that university information is fragmented across circulars, websites, and notice boards, wasting hours for both students and staff.",
        "<b>2. Live Demo (Student Chat):</b> Ask a natural question: <i>'What is the minimum attendance requirement to sit in semester exams?'</i> Show the instant answer, confidence score, and source citation.",
        "<b>3. Demonstrate Multi-turn Memory:</b> Ask a follow-up: <i>'What happens if I have medical leave?'</i> Show how it understands context.",
        "<b>4. Show the Fallback / Resiliency:</b> Explain how the dual engine protects against internet or quota drops.",
        "<b>5. Show the Admin Dashboard:</b> Log in as admin, show real-time query analytics, upload a notice, and show the unanswered query resolver.",
        "<b>6. Conclude with Future Scope:</b> Mention voice input (speech-to-text), multi-language regional support (Hindi/Tamil/Spanish), and WhatsApp/Telegram bot integrations."
    ]
    for item in checklist_items:
        story.append(Paragraph(item, bullet_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[Success] PDF generated: {filename}")

if __name__ == "__main__":
    out_path = sys.argv[1] if len(sys.argv) > 1 else "UniBot_Presentation_Defense_Guide.pdf"
    build_pdf(out_path)
