from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
import pandas as pd
from app.services.data_service import data_service
from app.services.analysis_service import analysis_service
from app.services.openai_service import openai_service

router = APIRouter()

class InsightsRequest(BaseModel):
    filename: str
    target_column: Optional[str] = None

class ExplainRequest(BaseModel):
    model_type: str
    metrics: Dict[str, Any]
    feature_importance: Optional[Dict[str, float]] = None

class QuestionRequest(BaseModel):
    question: str
    context: Dict[str, Any]

@router.get("/ai/status")
async def get_ai_status():
    """Check if OpenAI service is available"""
    return {
        "openai_available": openai_service.is_available(),
        "message": "OpenAI is available" if openai_service.is_available() else "OpenAI API key not configured"
    }

@router.post("/ai/insights")
async def get_ai_insights(request: InsightsRequest):
    """Get AI-powered insights about the data"""
    try:
        # Load data
        file_path = f"{data_service.data_path}/{request.filename}"
        try:
            df = pd.read_csv(file_path.replace(".csv", "_preprocessed.csv"))
        except:
            df = pd.read_csv(file_path)
        
        # Get standard analysis
        analysis_result = await analysis_service.analyze_data_context(df, request.target_column)
        
        # Prepare data summary
        data_summary = {
            "total_rows": len(df),
            "total_columns": len(df.columns),
            "numerical_columns": analysis_result.get("data_characteristics", {}).get("numerical_columns", 0),
            "categorical_columns": analysis_result.get("data_characteristics", {}).get("categorical_columns", 0),
            "missing_values": analysis_result.get("data_characteristics", {}).get("missing_values", 0),
        }
        
        # Generate AI insights if available
        ai_insights = None
        if openai_service.is_available():
            ai_insights = await openai_service.generate_data_insights(data_summary, analysis_result)
        
        return {
            "standard_analysis": analysis_result,
            "ai_insights": ai_insights,
            "ai_enabled": openai_service.is_available()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai/explain-model")
async def explain_model_results(request: ExplainRequest):
    """Get AI-powered explanation of model results"""
    if not openai_service.is_available():
        raise HTTPException(
            status_code=400, 
            detail="OpenAI service is not available. Please configure OPENAI_API_KEY."
        )
    
    try:
        explanation = await openai_service.explain_model_results(
            request.model_type,
            request.metrics,
            request.feature_importance
        )
        
        if not explanation:
            raise HTTPException(status_code=500, detail="Failed to generate explanation")
        
        return {
            "explanation": explanation,
            "model_type": request.model_type
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai/recommendations")
async def get_recommendations(
    problem_type: str,
    metrics: Dict[str, Any],
    has_missing_values: bool = False
):
    """Get AI-powered recommendations for next steps"""
    if not openai_service.is_available():
        raise HTTPException(
            status_code=400,
            detail="OpenAI service is not available. Please configure OPENAI_API_KEY."
        )
    
    try:
        recommendations = await openai_service.recommend_next_steps(
            problem_type,
            metrics,
            has_missing_values
        )
        
        if not recommendations:
            raise HTTPException(status_code=500, detail="Failed to generate recommendations")
        
        return {
            "recommendations": recommendations,
            "problem_type": problem_type
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai/ask")
async def ask_question(request: QuestionRequest):
    """Ask questions about your data or model"""
    if not openai_service.is_available():
        raise HTTPException(
            status_code=400,
            detail="OpenAI service is not available. Please configure OPENAI_API_KEY."
        )
    
    try:
        answer = await openai_service.answer_question(
            request.question,
            request.context
        )
        
        if not answer:
            raise HTTPException(status_code=500, detail="Failed to generate answer")
        
        return {
            "question": request.question,
            "answer": answer
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

