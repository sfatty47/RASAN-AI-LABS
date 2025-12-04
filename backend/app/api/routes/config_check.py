from fastapi import APIRouter
from app.config import settings
from app.services.openai_service import openai_service
import os

router = APIRouter()

@router.get("/config/check")
async def check_config():
    """Check configuration and environment variable loading"""
    # Check both os.getenv and settings
    os_key = os.getenv("OPENAI_API_KEY", "")
    settings_key = settings.OPENAI_API_KEY
    
    return {
        "from_os_env": {
            "has_key": bool(os_key and os_key.strip()),
            "key_length": len(os_key),
            "preview": os_key[:10] + "..." if os_key and len(os_key) > 10 else "empty"
        },
        "from_settings": {
            "has_key": bool(settings_key and settings_key.strip()),
            "key_length": len(settings_key),
            "preview": settings_key[:10] + "..." if settings_key and len(settings_key) > 10 else "empty"
        },
        "openai_service": {
            "enabled": openai_service.enabled,
            "available": openai_service.is_available(),
            "has_client": openai_service.client is not None
        },
        "debug_mode": settings.DEBUG
    }

