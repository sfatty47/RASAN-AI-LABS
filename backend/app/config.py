from pydantic_settings import BaseSettings
from typing import List
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Settings
    PORT: int = int(os.getenv("PORT", "8000"))
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    CORS_ORIGINS: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
    
    # ML Settings
    MAX_FILE_SIZE: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    MODEL_STORAGE_PATH: str = os.getenv("MODEL_STORAGE_PATH", "./models")
    DATA_STORAGE_PATH: str = os.getenv("DATA_STORAGE_PATH", "./data")
    
    # API Keys (modular - can be added later)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    HUGGINGFACE_API_KEY: str = os.getenv("HUGGINGFACE_API_KEY", "")
    HUGGINGFACE_TOKEN: str = os.getenv("HUGGINGFACE_TOKEN", "")
    
    # Training Settings
    MAX_TRAINING_TIME: int = int(os.getenv("MAX_TRAINING_TIME", "3600"))  # 1 hour
    N_JOBS: int = int(os.getenv("N_JOBS", "-1"))  # Use all CPUs
    
    class Config:
        # Try multiple .env file locations
        env_file = [
            ".env",  # Current directory
            Path(__file__).parent.parent.parent / ".env",  # Backend directory
            Path(__file__).parent.parent / ".env",  # App directory (fallback)
        ]
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()

# Debug: Check if OpenAI key is loaded (only in debug mode)
if settings.DEBUG:
    has_openai_key = bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip())
    print(f"[DEBUG] OpenAI API Key loaded: {has_openai_key}")
    if has_openai_key:
        print(f"[DEBUG] OpenAI API Key starts with: {settings.OPENAI_API_KEY[:7]}...")
