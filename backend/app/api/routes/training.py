from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import pandas as pd
from app.services.data_service import data_service
from app.ml.trainer import model_trainer

router = APIRouter()

class TrainRequest(BaseModel):
    filename: str
    target: str
    problem_type: str
    model_name: Optional[str] = None
    features: Optional[List[str]] = None

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
            raise HTTPException(status_code=500, detail=result.get("error", "Training failed"))
        
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
