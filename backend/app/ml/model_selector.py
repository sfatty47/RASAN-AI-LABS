import pandas as pd
from typing import Dict, Any, Optional, List

class ModelSelector:
    async def select_models(
        self,
        df: pd.DataFrame,
        target: str,
        problem_type: str,
        features: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Smart model selection based on problem type and data characteristics"""
        selection = {
            "problem_type": problem_type,
            "recommended_models": [],
            "selection_criteria": {}
        }
        
        if problem_type == "Regression":
            selection["recommended_models"] = [
                {"name": "Linear Regression", "priority": 1},
                {"name": "Random Forest", "priority": 2},
                {"name": "XGBoost", "priority": 3},
                {"name": "LightGBM", "priority": 4},
                {"name": "CatBoost", "priority": 5}
            ]
        elif problem_type == "Binary Classification":
            selection["recommended_models"] = [
                {"name": "Logistic Regression", "priority": 1},
                {"name": "Random Forest", "priority": 2},
                {"name": "XGBoost", "priority": 3},
                {"name": "LightGBM", "priority": 4}
            ]
        elif problem_type == "Multi-class Classification":
            selection["recommended_models"] = [
                {"name": "Random Forest", "priority": 1},
                {"name": "XGBoost", "priority": 2},
                {"name": "LightGBM", "priority": 3}
            ]
        
        # Add selection criteria based on data size
        n_samples = len(df)
        if n_samples < 1000:
            selection["selection_criteria"]["note"] = "Small dataset - simpler models recommended"
        elif n_samples > 100000:
            selection["selection_criteria"]["note"] = "Large dataset - gradient boosting models recommended"
        
        return selection

model_selector = ModelSelector()
