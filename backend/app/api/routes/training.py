from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
from app.services.data_service import data_service
from app.ml.trainer import model_trainer
from app.config import settings

router = APIRouter()

class TrainRequest(BaseModel):
    filename: str
    target: str
    problem_type: str
    model_name: Optional[str] = None
    features: Optional[List[str]] = None

@router.get("/train/status")
async def training_status():
    """Check training system status"""
    try:
        # Check if directories exist
        import os
        data_dir_exists = os.path.exists(data_service.data_path)
        model_dir_exists = os.path.exists(data_service.data_path.replace("data", "models"))
        
        return {
            "status": "ready",
            "data_path": data_service.data_path,
            "model_path": settings.MODEL_STORAGE_PATH,
            "data_dir_exists": data_dir_exists,
            "model_dir_exists": model_dir_exists,
            "n_jobs": settings.N_JOBS
        }
    except Exception as e:
        return {
            "status": "error",
            "error": str(e)
        }

@router.post("/train")
async def train_model(request: TrainRequest):
    """Train a model with automated tuning"""
    try:
        # Load the preprocessed data
        file_path = f"{data_service.data_path}/{request.filename}"
        # Try preprocessed version first, then original
        preprocessed_path = file_path.replace(".csv", "_preprocessed.csv")
        try:
            df = pd.read_csv(preprocessed_path)
        except FileNotFoundError:
            df = pd.read_csv(file_path)
        
        # Validate target column exists
        if request.target not in df.columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Target column '{request.target}' not found in dataset"
            )
        
        # Train the model
        result = await model_trainer.train(
            df=df,
            target=request.target,
            problem_type=request.problem_type,
            model_name=request.model_name,
            features=request.features
        )
        
        if result.get("status") == "failed":
            error_msg = result.get("error", "Training failed")
            error_details = result.get("details", {})
            full_error = f"{error_msg}"
            if error_details.get("error_type"):
                full_error += f" ({error_details['error_type']})"
            raise HTTPException(status_code=500, detail=full_error)
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
