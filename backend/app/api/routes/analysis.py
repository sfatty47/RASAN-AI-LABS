from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import pandas as pd
from app.services.analysis_service import analysis_service
from app.services.data_service import data_service
from app.services.openai_service import openai_service

router = APIRouter()

class AnalysisRequest(BaseModel):
    filename: str
    target_column: Optional[str] = None

@router.post("/analyze")
async def analyze_data(request: AnalysisRequest):
    """Smart data analysis with optional AI insights"""
    file_path = f"{data_service.data_path}/{request.filename}"
    try:
        df = pd.read_csv(file_path)
        result = await analysis_service.analyze_data_context(df, request.target_column)
        
        # Add AI insights if OpenAI is available
        ai_insights = None
        if openai_service.is_available():
            data_summary = {
                "total_rows": len(df),
                "total_columns": len(df.columns),
                "numerical_columns": result.get("data_characteristics", {}).get("numerical_columns", 0),
                "categorical_columns": result.get("data_characteristics", {}).get("categorical_columns", 0),
                "missing_values": result.get("data_characteristics", {}).get("missing_values", 0),
            }
            ai_insights = await openai_service.generate_data_insights(data_summary, result)
        
        result["ai_insights"] = ai_insights
        result["ai_enabled"] = openai_service.is_available()
        
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
