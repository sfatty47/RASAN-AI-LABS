from fastapi import APIRouter, HTTPException
from pathlib import Path
import os

router = APIRouter()

@router.get("/debug/frontend-check")
async def check_frontend():
    """Debug endpoint to check if frontend files exist"""
    checks = {}
    
    # Check Docker path
    docker_path = Path("/app/frontend/dist")
    checks["docker_path"] = {
        "path": str(docker_path),
        "exists": docker_path.exists(),
        "is_dir": docker_path.is_dir() if docker_path.exists() else False
    }
    
    # Check for index.html
    if docker_path.exists():
        index_file = docker_path / "index.html"
        checks["index_html"] = {
            "path": str(index_file),
            "exists": index_file.exists()
        }
        
        # List directory contents
        try:
            contents = list(docker_path.iterdir())
            checks["directory_contents"] = [str(p.name) for p in contents]
        except Exception as e:
            checks["directory_contents_error"] = str(e)
        
        # Check for assets directory
        assets_dir = docker_path / "assets"
        checks["assets_dir"] = {
            "path": str(assets_dir),
            "exists": assets_dir.exists(),
            "is_dir": assets_dir.is_dir() if assets_dir.exists() else False
        }
        
        if assets_dir.exists():
            try:
                asset_files = list(assets_dir.iterdir())
                checks["asset_files"] = [str(p.name) for p in asset_files[:10]]  # First 10
            except Exception as e:
                checks["asset_files_error"] = str(e)
    
    # Check environment
    checks["environment"] = {
        "PYTHONPATH": os.environ.get("PYTHONPATH", "not set"),
        "PORT": os.environ.get("PORT", "not set"),
        "working_dir": os.getcwd()
    }
    
    # Check app directory structure
    app_dir = Path("/app")
    if app_dir.exists():
        try:
            app_contents = [p.name for p in app_dir.iterdir() if p.is_dir()]
            checks["app_directory_structure"] = app_contents
        except Exception as e:
            checks["app_directory_error"] = str(e)
    
    return {
        "status": "success",
        "checks": checks,
        "frontend_available": checks.get("index_html", {}).get("exists", False)
    }

@router.get("/debug/env")
async def debug_env():
    """Debug endpoint to check environment variables"""
    return {
        "PORT": os.environ.get("PORT"),
        "PYTHONPATH": os.environ.get("PYTHONPATH"),
        "working_dir": os.getcwd(),
        "all_env": {k: v for k, v in os.environ.items() if not k.startswith("RAILWAY_")}
    }
