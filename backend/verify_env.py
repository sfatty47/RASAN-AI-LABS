#!/usr/bin/env python3
"""Verify .env file contents"""
import os
from pathlib import Path

env_file = Path('.env')
print("🔍 Checking .env file...")
print(f"File exists: {env_file.exists()}")
print(f"File size: {env_file.stat().st_size} bytes")
print()

if env_file.exists():
    with open(env_file, 'r') as f:
        content = f.read()
        print("File contents:")
        print("=" * 50)
        for i, line in enumerate(content.splitlines(), 1):
            if 'OPENAI_API_KEY' in line:
                print(f"Line {i}: {repr(line)}")
                parts = line.split('=', 1)
                if len(parts) == 2:
                    value = parts[1].strip()
                    print(f"  Value: {repr(value)}")
                    print(f"  Length: {len(value)} chars")
                    if value:
                        print(f"  ✅ KEY IS SET!")
                        print(f"  Preview: {value[:15]}...")
                    else:
                        print(f"  ❌ KEY IS EMPTY")
                break
        print("=" * 50)

