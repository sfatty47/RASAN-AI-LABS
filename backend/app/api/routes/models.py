from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from app.services.model_service import model_service

router = APIRouter()

class PredictRequest(BaseModel):
    model_id: str
    data: Dict[str, Any]

@router.get("/models/{model_id}")
async def get_model(model_id: str):
    """Get model information"""
    try:
        model = await model_service.load_model(model_id)
        return {"model_id": model_id, "status": "loaded"}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/predict")
async def predict(request: PredictRequest):
    """Make predictions"""
    try:
        result = await model_service.predict(request.model_id, request.data)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
