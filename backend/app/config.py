from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
from pathlib import Path
import os

# Get the backend directory (parent of app directory)
BACKEND_DIR = Path(__file__).parent.parent.parent
ENV_FILE = BACKEND_DIR / ".env"

class Settings(BaseSettings):
    # API Settings
    PORT: int = 8000
    DEBUG: bool = False
    CORS_ORIGINS: str = "http://localhost:3000"
    
    # ML Settings
    MAX_FILE_SIZE: int = 10485760  # 10MB
    MODEL_STORAGE_PATH: str = "./models"
    DATA_STORAGE_PATH: str = "./data"
    
    # API Keys (modular - can be added later)
    OPENAI_API_KEY: str = ""
    HUGGINGFACE_API_KEY: str = ""
    HUGGINGFACE_TOKEN: str = ""
    
    # Training Settings
    MAX_TRAINING_TIME: int = 3600  # 1 hour
    N_JOBS: int = -1  # Use all CPUs
    
    model_config = SettingsConfigDict(
        # Try multiple locations for .env file
        env_file=str(ENV_FILE) if ENV_FILE.exists() else ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
        # Also check environment variables
        env_ignore_empty=True
    )
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS_ORIGINS string into list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]

settings = Settings()
