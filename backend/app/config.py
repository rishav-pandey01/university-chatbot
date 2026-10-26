from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pathlib import Path
import os

# Locate .env whether run from backend/ or project root
_BACKEND_DIR = Path(__file__).resolve().parent.parent
_PROJECT_DIR = _BACKEND_DIR.parent
_ENV_CANDIDATES = [
    _BACKEND_DIR / ".env",
    _PROJECT_DIR / ".env",
    Path(".env").resolve(),
]
_ENV_FILE = next((str(p) for p in _ENV_CANDIDATES if p.is_file()), ".env")

class Settings(BaseSettings):
    PROJECT_NAME: str = "University Student Support AI Chatbot"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api"
    
    # Security
    SECRET_KEY: str = "super-secret-university-chatbot-jwt-key-change-in-prod-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    
    # Database
    DATABASE_URL: str = "sqlite:///./university_chatbot.db"
    
    # AI / LLM Integration (Valid Gemini models: gemini-2.5-flash, gemini-1.5-flash, gemini-2.0-flash)
    GEMINI_API_KEY: str = ""
    GEMINI_MODEL: str = "gemini-2.5-flash"
    
    # RAG Settings
    SIMILARITY_THRESHOLD: float = 0.25
    MAX_RETRIEVED_CHUNKS: int = 4
    
    # Storage
    UPLOAD_DIR: str = "uploads"
    MAX_UPLOAD_SIZE_MB: int = 15
    
    # CORS
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000"
    ]

    model_config = SettingsConfigDict(
        env_file=_ENV_FILE,
        env_file_encoding="utf-8",
        extra="allow"
    )

settings = Settings()
