import pandas as pd
import numpy as np
from typing import Dict, Any, Optional
from scipy import stats

class AnalysisService:
    async def analyze_data_context(self, df: pd.DataFrame, target_column: Optional[str] = None) -> Dict[str, Any]:
        """Smart analysis to determine problem type and approach"""
        analysis_results = {
            "problem_type": None,
            "suitable_approaches": [],
            "data_characteristics": {},
            "recommended_visualizations": [],
            "target_column": target_column
        }
        
        # Analyze target variable if provided
        if target_column and target_column in df.columns:
            target = df[target_column]
            unique_count = target.nunique()
            
            if unique_count == 2:
                analysis_results["problem_type"] = "Binary Classification"
                analysis_results["suitable_approaches"] = [
                    "Logistic Regression",
                    "Decision Trees",
                    "Random Forest",
                    "XGBoost",
                    "LightGBM"
                ]
            elif 2 < unique_count < 20:
                analysis_results["problem_type"] = "Multi-class Classification"
                analysis_results["suitable_approaches"] = [
                    "Multi-class Classification",
                    "Decision Trees",
                    "Random Forest",
                    "XGBoost",
                    "LightGBM"
                ]
            else:
                analysis_results["problem_type"] = "Regression"
                analysis_results["suitable_approaches"] = [
                    "Linear Regression",
                    "Random Forest",
                    "XGBoost",
                    "LightGBM",
                    "CatBoost"
                ]
        
        # Check for A/B test potential
        if "group" in df.columns and "outcome" in df.columns:
            analysis_results["suitable_approaches"].append("A/B Testing")
        
        # Data characteristics
        numerical_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        
        analysis_results["data_characteristics"] = {
            "numerical_columns": len(numerical_cols),
            "categorical_columns": len(categorical_cols),
            "missing_values": int(df.isnull().sum().sum()),
            "total_rows": len(df),
            "total_columns": len(df.columns)
        }
        
        # Recommended visualizations
        if analysis_results["problem_type"] == "Regression":
            analysis_results["recommended_visualizations"] = [
                "Scatter Plot",
                "Residual Plot",
                "Feature Importance",
                "Correlation Heatmap"
            ]
        elif analysis_results["problem_type"] in ["Binary Classification", "Multi-class Classification"]:
            analysis_results["recommended_visualizations"] = [
                "Confusion Matrix",
                "ROC Curve",
                "Feature Importance",
                "Target Distribution"
            ]
        
        return analysis_results
    
    async def perform_ab_test(self, df: pd.DataFrame) -> Optional[Dict[str, Any]]:
        """Perform A/B testing if applicable"""
        if "group" in df.columns and "outcome" in df.columns:
            group_a = df[df["group"] == "A"]["outcome"]
            group_b = df[df["group"] == "B"]["outcome"]
            
            if len(group_a) > 0 and len(group_b) > 0:
                t_stat, p_value = stats.ttest_ind(group_a, group_b)
                
                return {
                    "t_statistic": float(t_stat),
                    "p_value": float(p_value),
                    "significant": p_value < 0.05,
                    "group_a_mean": float(group_a.mean()),
                    "group_b_mean": float(group_b.mean()),
                    "group_a_size": len(group_a),
                    "group_b_size": len(group_b)
                }
        return None

analysis_service = AnalysisService()
