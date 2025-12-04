from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import pandas as pd
from app.services.analysis_service import analysis_service
from app.services.data_service import data_service

router = APIRouter()

class AnalysisRequest(BaseModel):
    filename: str
    target_column: Optional[str] = None

@router.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    """Smart data analysis"""
    file_path = f"{data_service.data_path}/{request.filename}"
    try:
        df = pd.read_csv(file_path)
        result = await analysis_service.analyze_data_context(df, request.target_column)
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
