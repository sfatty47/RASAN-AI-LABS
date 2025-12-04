from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np
from app.services.model_service import model_service
from app.services.data_service import data_service
from app.services.visualization_service import visualization_service
import asyncio

router = APIRouter()

@router.post("/visualizations/{model_id}/predict-and-visualize")
async def predict_and_visualize(
    model_id: str,
    filename: str,
    target_column: str,
    chart_types: Optional[List[str]] = None
):
    """Generate predictions and create visualizations"""
    try:
        # Load model
        model_info = await model_service.load_model(model_id)
        problem_type = model_info.get("model_type", "Regression")
        loaded_model = model_service._loaded_models[model_id]["model"]
        
        # Load and prepare data
        file_path = f"{data_service.data_path}/{filename}"
        try:
            df = pd.read_csv(file_path.replace(".csv", "_preprocessed.csv"))
        except:
            df = pd.read_csv(file_path)
        
        # Separate features and target
        if target_column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Target column '{target_column}' not found")
        
        X = df.drop(columns=[target_column])
        y_true = df[target_column].values
        
        # Use model.predict directly for predictions
        loop = asyncio.get_event_loop()
        
        # Get predictions using the model's predict method
        y_pred = await loop.run_in_executor(
            None,
            lambda: loaded_model.predict(X)
        )
        
        # Convert to numpy array if needed
        if isinstance(y_pred, pd.Series):
            y_pred = y_pred.values
        elif isinstance(y_pred, list):
            y_pred = np.array(y_pred)
        
        # Try to get probabilities for classification
        y_pred_proba = None
        if problem_type != "Regression":
            try:
                if hasattr(loaded_model, 'predict_proba'):
                    y_pred_proba = await loop.run_in_executor(
                        None,
                        lambda: loaded_model.predict_proba(X)
                    )
            except Exception as e:
                print(f"Could not get probabilities: {e}")
        
        # Determine default chart types
        if chart_types is None:
            if problem_type == "Regression":
                chart_types = ["feature_importance", "prediction_distribution", "regression_metrics", "correlation_heatmap"]
            else:
                chart_types = ["feature_importance", "confusion_matrix", "classification_metrics", "prediction_distribution"]
                if y_pred_proba is not None:
                    chart_types.append("roc_curve")
        
        # Generate visualizations
        visualizations = {}
        
        # Feature Importance
        if "feature_importance" in chart_types:
            try:
                visualizations["feature_importance"] = visualization_service.generate_feature_importance(loaded_model, X)
            except Exception as e:
                visualizations["feature_importance"] = {"error": str(e)}
        
        # Correlation Heatmap
        if "correlation_heatmap" in chart_types:
            try:
                visualizations["correlation_heatmap"] = visualization_service.generate_correlation_heatmap(df)
            except Exception as e:
                visualizations["correlation_heatmap"] = {"error": str(e)}
        
        # Classification-specific charts
        if problem_type != "Regression":
            if "confusion_matrix" in chart_types:
                try:
                    visualizations["confusion_matrix"] = visualization_service.generate_confusion_matrix(y_true, y_pred)
                except Exception as e:
                    visualizations["confusion_matrix"] = {"error": str(e)}
            
            if "roc_curve" in chart_types and y_pred_proba is not None:
                try:
                    visualizations["roc_curve"] = visualization_service.generate_roc_curve(y_true, y_pred_proba)
                except Exception as e:
                    visualizations["roc_curve"] = {"error": str(e)}
            
            if "classification_metrics" in chart_types:
                try:
                    visualizations["classification_metrics"] = visualization_service.generate_classification_metrics(y_true, y_pred)
                except Exception as e:
                    visualizations["classification_metrics"] = {"error": str(e)}
        
        # Regression-specific charts
        if problem_type == "Regression":
            if "regression_metrics" in chart_types:
                try:
                    visualizations["regression_metrics"] = visualization_service.generate_regression_metrics(y_true, y_pred)
                except Exception as e:
                    visualizations["regression_metrics"] = {"error": str(e)}
        
        # Prediction distribution
        if "prediction_distribution" in chart_types:
            try:
                visualizations["prediction_distribution"] = visualization_service.generate_prediction_distribution(
                    y_true, y_pred, problem_type
                )
            except Exception as e:
                visualizations["prediction_distribution"] = {"error": str(e)}
        
        return {
            "model_id": model_id,
            "problem_type": problem_type,
            "visualizations": visualizations,
            "predictions": {
                "y_true": y_true.tolist()[:100],  # Limit for response size
                "y_pred": y_pred.tolist()[:100] if isinstance(y_pred, np.ndarray) else y_pred[:100]
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        raise HTTPException(status_code=500, detail=f"Visualization generation failed: {str(e)}\n{traceback.format_exc()}")
