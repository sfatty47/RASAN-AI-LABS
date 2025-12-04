import pandas as pd
from pathlib import Path
from typing import Dict, Any
from pycaret.regression import load_model as load_model_reg
from pycaret.classification import load_model as load_model_clf
import shap
import numpy as np

class ModelEvaluator:
    async def evaluate(self, model_path: str, test_data_path: str) -> Dict[str, Any]:
        """Generate comprehensive evaluation report"""
        try:
            # Load model and test data
            model = load_model_reg(model_path) if "regression" in model_path else load_model_clf(model_path)
            test_df = pd.read_csv(test_data_path)
            
            # Generate SHAP values for interpretability
            explainer = shap.TreeExplainer(model)
            shap_values = explainer.shap_values(test_df)
            
            # Feature importance
            if isinstance(shap_values, list):
                feature_importance = np.abs(shap_values[0]).mean(0)
            else:
                feature_importance = np.abs(shap_values).mean(0)
            
            importance_dict = {
                col: float(importance)
                for col, importance in zip(test_df.columns, feature_importance)
            }
            
            return {
                "model_path": model_path,
                "feature_importance": importance_dict,
                "evaluation_status": "completed"
            }
        except Exception as e:
            return {
                "evaluation_status": "failed",
                "error": str(e)
            }

model_evaluator = ModelEvaluator()
