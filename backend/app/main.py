from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from app.config import settings
from app.api.routes import upload, analysis, training, models, visualizations, ai_insights, config_check

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

@app.get("/")
async def root():
    return {"message": "RASAN AI Labs API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG
    )
