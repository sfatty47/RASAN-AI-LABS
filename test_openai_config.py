#!/usr/bin/env python3
"""Quick test to verify OpenAI API key is loaded"""
import sys
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

from app.config import settings
from app.services.openai_service import openai_service

print("🔍 Testing OpenAI Configuration")
print("=" * 40)
print()

key = settings.OPENAI_API_KEY
has_key = bool(key and key.strip())

print(f"API Key Status: {'✅ SET' if has_key else '❌ EMPTY'}")
if has_key:
    print(f"Key Length: {len(key)} characters")
    print(f"Preview: {key[:10]}...")
    print(f"OpenAI Service Enabled: {openai_service.enabled}")
    print(f"OpenAI Service Available: {openai_service.is_available()}")
else:
    print("⚠️  Key is empty or not loaded")
    print()
    print("Possible issues:")
    print("1. Key not in backend/.env file")
    print("2. Backend server not restarted after adding key")
    print("3. .env file format issue")

