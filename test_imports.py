#!/usr/bin/env python3
"""
Smoke test script to verify all imports and structure
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent / "backend"))

errors = []
warnings = []

def check_file_exists(filepath, description):
    """Check if a file exists"""
    if not os.path.exists(filepath):
        errors.append(f"❌ Missing: {description} at {filepath}")
        return False
    return True

def check_file_not_empty(filepath, description):
    """Check if a file is not empty"""
    if os.path.exists(filepath):
        with open(filepath, 'r') as f:
            content = f.read().strip()
            if not content or len(content) < 10:
                errors.append(f"❌ Empty or too short: {description} at {filepath}")
                return False
    return True

def check_has_router(filepath, module_name):
    """Check if a route file has router attribute"""
    try:
        content = open(filepath).read()
        if 'router = APIRouter()' not in content and 'router=APIRouter()' not in content:
            errors.append(f"❌ Missing router: {module_name} at {filepath}")
            return False
    except Exception as e:
        errors.append(f"❌ Error checking router: {module_name} - {e}")
        return False
    return True

print("🔍 Running smoke test...\n")

# Check all route files have routers
route_files = [
    ("backend/app/api/routes/upload.py", "upload"),
    ("backend/app/api/routes/analysis.py", "analysis"),
    ("backend/app/api/routes/training.py", "training"),
    ("backend/app/api/routes/models.py", "models"),
]

print("📁 Checking route files...")
for filepath, name in route_files:
    if check_file_exists(filepath, f"{name} route"):
        check_file_not_empty(filepath, f"{name} route")
        check_has_router(filepath, name)

# Check all service files exist and are not empty
service_files = [
    ("backend/app/services/data_service.py", "DataService"),
    ("backend/app/services/analysis_service.py", "AnalysisService"),
    ("backend/app/services/model_service.py", "ModelService"),
]

print("\n🔧 Checking service files...")
for filepath, name in service_files:
    if check_file_exists(filepath, f"{name}"):
        check_file_not_empty(filepath, f"{name}")

# Check all ML files exist
ml_files = [
    ("backend/app/ml/trainer.py", "ModelTrainer"),
    ("backend/app/ml/evaluator.py", "ModelEvaluator"),
    ("backend/app/ml/model_selector.py", "ModelSelector"),
]

print("\n🤖 Checking ML files...")
for filepath, name in ml_files:
    if check_file_exists(filepath, f"{name}"):
        check_file_not_empty(filepath, f"{name}")

# Check critical files
critical_files = [
    ("backend/app/main.py", "main.py"),
    ("backend/app/config.py", "config.py"),
    ("backend/app/models/schemas.py", "schemas.py"),
]

print("\n📄 Checking critical files...")
for filepath, name in critical_files:
    check_file_exists(filepath, name)
    if os.path.exists(filepath):
        check_file_not_empty(filepath, name)

# Check __init__.py files
init_files = [
    "backend/app/__init__.py",
    "backend/app/api/__init__.py",
    "backend/app/api/routes/__init__.py",
    "backend/app/services/__init__.py",
    "backend/app/ml/__init__.py",
    "backend/app/models/__init__.py",
]

print("\n📦 Checking __init__.py files...")
for filepath in init_files:
    check_file_exists(filepath, "__init__.py")

# Check for router imports in main.py
print("\n🔗 Checking main.py imports...")
if os.path.exists("backend/app/main.py"):
    with open("backend/app/main.py") as f:
        main_content = f.read()
        required_routers = ["upload", "analysis", "training", "models"]
        for router_name in required_routers:
            if f"import {router_name}" not in main_content and f", {router_name}" not in main_content:
                errors.append(f"❌ Missing import in main.py: {router_name}")

print("\n" + "="*60)
if errors:
    print(f"❌ Found {len(errors)} error(s):")
    for error in errors:
        print(f"  {error}")
    sys.exit(1)
else:
    print("✅ All checks passed! No errors found.")
    sys.exit(0)

