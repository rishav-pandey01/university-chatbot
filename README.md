# 🎓 UniBot — AI-Powered University Student Support System

An end-to-end intelligent chatbot and student support web application built with **FastAPI**, **React 19**, **Vite**, and **Google Gemini 3.8 Flash** with local RAG semantic fallback.

---

## ✨ Features

- 💬 **Intelligent Chatbot & RAG**: Context-grounded responses with confidence scoring, document source citations, follow-up suggestions, and thumbs-up/down feedback.
- 🔄 **Dual Engine Architecture**: Powers answers via Gemini 3.8 Flash when configured, or seamlessly falls back to the built-in TF-IDF/BM25 semantic retriever without requiring any external API key.
- 📚 **FAQ Knowledge Base**: Categorized and searchable FAQ explorer with responsive accordion view and keyword tagging.
- 📢 **Campus Notices & Announcements**: Real-time university bulletin board with priority (Urgent/Normal) flags.
- 📊 **Comprehensive Admin Dashboard**:
  - Live analytics & KPI metrics (total queries, active conversations, satisfaction rate, fallback rate)
  - Category distribution visualizer
  - FAQ CRUD manager
  - Notice & Announcement publisher
  - Document uploader (PDF, TXT, MD) with automatic text extraction & chunking
  - Unanswered / Fallback query resolver
  - Student feedback audit log
- 🔐 **JWT Authentication & Role Control**: Multi-role support (`student` and `admin`) with guest access allowed for anonymous chat queries.

---

## 🏛️ Project Structure

```
Chatbot university student/
├── backend/
│   ├── app/
│   │   ├── api/             # FastAPI REST endpoints (auth, chat, faqs, documents, etc.)
│   │   ├── core/            # Security (bcrypt, JWT) and FastAPI dependencies
│   │   ├── models/          # SQLAlchemy ORM models (User, Conversation, Message, FAQ, etc.)
│   │   ├── rag/             # Retrieval-Augmented Generation pipeline & fallback synthesizer
│   │   ├── schemas/         # Pydantic v2 validation models
│   │   ├── config.py        # Centralized settings
│   │   ├── database.py      # SQLAlchemy engine and session factory
│   │   ├── init_db.py       # Database schema initialization & seed data
│   │   └── main.py          # FastAPI application entrypoint
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
├── frontend/
│   ├── src/
│   │   ├── components/      # Navbar, Layout, and UI widgets
│   │   ├── context/         # AuthContext (JWT management & session state)
│   │   ├── pages/           # HomePage, ChatPage, FAQPage, AnnouncementsPage, AdminPage, Auth
│   │   ├── api.js           # Axios client with interceptors
│   │   ├── App.jsx          # Route definitions & protected routes
│   │   ├── App.css          # University academic blue & white design system
│   │   └── index.css        # Core tokens, typography, and base resets
│   ├── package.json
│   └── vite.config.js       # Vite dev server with proxy to :8000
└── README.md
```

---

## 🚀 Getting Started

### 1. Start the Backend

1. Open a terminal in the `backend` folder:
   ```powershell
   cd backend
   ```
2. Activate the virtual environment:
   ```powershell
   ..\.venv\Scripts\activate
   ```
3. (Optional) Add your Gemini API key in `backend/.env`:
   ```env
   GEMINI_API_KEY="your-gemini-api-key"
   ```
   *(If left empty, the application runs on the built-in intelligent RAG synthesizer!)*

4. Run the FastAPI server:
   ```powershell
   python -m uvicorn app.main:app --reload --port 8000
   ```
   - API Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
   - Health check: [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

### 2. Start the Frontend

1. Open another terminal in the `frontend` folder:
   ```powershell
   cd frontend
   ```
2. Start the Vite development server:
   ```powershell
   cmd /c npm run dev
   ```
3. Open your browser at **`http://localhost:5173`**.

---

## 🔑 Pre-Seeded Demo Accounts

The database comes pre-seeded with sample FAQs, university policies, announcements, and demo users:

| Role | Email | Password | Access |
|---|---|---|---|
| **Administrator** | `admin@university.edu` | `Admin@123` | Full access + Admin Dashboard (`/admin`) |
| **Student** | `student@university.edu` | `Student@123` | Student access + Chat history |

*(You can also register a new student account directly from the UI or use the chat anonymously.)*
