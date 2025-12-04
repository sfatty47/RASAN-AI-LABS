from fastapi import APIRouter
from app.config import settings
from app.services.openai_service import openai_service

router = APIRouter()

@router.get("/debug/env")
async def debug_env():
    """Debug endpoint to check environment variables (only in debug mode)"""
    return {
        "debug_mode": settings.DEBUG,
        "openai_key_configured": bool(settings.OPENAI_API_KEY and settings.OPENAI_API_KEY.strip()),
        "openai_key_length": len(settings.OPENAI_API_KEY) if settings.OPENAI_API_KEY else 0,
        "openai_key_preview": settings.OPENAI_API_KEY[:10] + "..." if settings.OPENAI_API_KEY and len(settings.OPENAI_API_KEY) > 10 else "not set",
        "openai_service_available": openai_service.is_available(),
        "openai_service_enabled": openai_service.enabled,
    }

