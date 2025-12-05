from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn
from app.config import settings
from app.api.routes import upload, analysis, training, models, visualizations, ai_insights, config_check, debug

app = FastAPI(
    title="RASAN AI Labs API",
    description="AI-Powered AutoML Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router, prefix="/api/v1", tags=["upload"])
app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])
app.include_router(training.router, prefix="/api/v1", tags=["training"])
app.include_router(models.router, prefix="/api/v1", tags=["models"])
app.include_router(visualizations.router, prefix="/api/v1", tags=["visualizations"])
app.include_router(ai_insights.router, prefix="/api/v1", tags=["ai-insights"])
app.include_router(config_check.router, prefix="/api/v1", tags=["config"])
app.include_router(debug.router, prefix="/api/v1", tags=["debug"])

# Serve static files from frontend build (if it exists)
# Check both possible locations: relative to app dir and in /app/frontend/dist
import logging

logger = logging.getLogger(__name__)

_frontend_dist_local = Path(__file__).parent.parent.parent.parent / "frontend" / "dist"
_frontend_dist_docker = Path("/app/frontend/dist")

logger.info(f"Checking for frontend at: {_frontend_dist_docker}")
logger.info(f"Also checking: {_frontend_dist_local}")

if _frontend_dist_docker.exists():
    frontend_dist = _frontend_dist_docker
    logger.info(f"✅ Found frontend at Docker path: {frontend_dist}")
elif _frontend_dist_local.exists():
    frontend_dist = _frontend_dist_local
    logger.info(f"✅ Found frontend at local path: {frontend_dist}")
else:
    frontend_dist = None
    logger.warning("⚠️ Frontend dist directory not found! Serving API only.")

frontend_index = frontend_dist / "index.html" if frontend_dist else None

if frontend_dist and frontend_index and frontend_index.exists():
    logger.info(f"✅ Frontend index.html found at: {frontend_index}")
    # Mount static assets (JS, CSS, images, etc.)
    assets_dir = frontend_dist / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")
        logger.info(f"✅ Static assets mounted at /assets")
    
    # Serve other static files
    static_files_dir = frontend_dist
    _static_files = ["favicon.ico", "robots.txt", "manifest.json"]
    for static_file in _static_files:
        static_path = static_files_dir / static_file
        if static_path.exists():
            # Create route handler with closure to capture file path
            def make_static_handler(file_path: Path):
                async def handler():
                    return FileResponse(str(file_path))
                return handler
            
            app.get(f"/{static_file}")(make_static_handler(static_path))
else:
    logger.warning("⚠️ Frontend index.html not found! Root route will return API info.")

@app.get("/")
async def root():
    """Serve frontend index.html or API info"""
    if frontend_index and frontend_index.exists():
        logger.info("Serving frontend index.html")
        return FileResponse(str(frontend_index), media_type="text/html")
    logger.info("Frontend not found, serving API info")
    return {"message": "RASAN AI Labs API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Catch-all route for SPA routing - must be last
@app.get("/{full_path:path}")
async def serve_spa(full_path: str):
    """
    Serve the React app for all non-API routes.
    This enables client-side routing for the SPA.
    """
    # Don't interfere with API routes
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Don't interfere with static assets
    if full_path.startswith("assets/"):
        raise HTTPException(status_code=404, detail="Asset not found")
    
    # Serve index.html for all other routes (SPA routing)
    if frontend_index and frontend_index.exists():
        return FileResponse(str(frontend_index))
    
    raise HTTPException(status_code=404, detail="Frontend not built. Please build the frontend first.")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG
    )
