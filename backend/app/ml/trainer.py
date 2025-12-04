import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional, List
from pycaret.regression import setup as setup_reg, compare_models as compare_models_reg, pull, save_model, tune_model
from pycaret.classification import setup as setup_clf, compare_models as compare_models_clf, tune_model as tune_model_clf
from app.config import settings
import asyncio

class ModelTrainer:
    async def train(
        self,
        df: pd.DataFrame,
        target: str,
        problem_type: str,
        model_name: Optional[str] = None,
        features: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Train and tune model with hyperparameter optimization"""
        # Run in executor to avoid blocking
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            self._train_sync,
            df, target, problem_type, model_name, features
        )
        return result
    
    def _train_sync(
        self,
        df: pd.DataFrame,
        target: str,
        problem_type: str,
        model_name: Optional[str] = None,
        features: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Synchronous training function"""
        try:
            # Validate input data
            if df.empty:
                raise ValueError("Dataset is empty")
            
            if target not in df.columns:
                raise ValueError(f"Target column '{target}' not found in dataset. Available columns: {list(df.columns)}")
            
            # Check for missing values in target
            missing_target = df[target].isnull().sum()
            if missing_target > 0:
                # Remove rows with missing target values
                df = df.dropna(subset=[target])
                if df.empty:
                    raise ValueError(f"After removing rows with missing target values, dataset is empty")
            
            # Select features if specified
            if features:
                missing_features = [f for f in features if f not in df.columns]
                if missing_features:
                    raise ValueError(f"Features not found in dataset: {missing_features}")
                df = df[features + [target]]
            
            # Ensure model storage directory exists
            model_path = Path(settings.MODEL_STORAGE_PATH)
            model_path.mkdir(parents=True, exist_ok=True)
            
            # Normalize problem type for PyCaret (handle variations)
            is_classification = problem_type.lower() in ["binary classification", "multi-class classification", "classification"]
            
            # Setup PyCaret - use only supported parameters for 3.3.0
            if not is_classification:  # Regression
                setup_reg(df, target=target, n_jobs=settings.N_JOBS)
                best_model = compare_models_reg()
                # Hyperparameter tuning - skip if model doesn't support it
                try:
                    tuned_model = tune_model(best_model, n_iter=10)
                except (ValueError, TypeError) as tune_error:
                    # If tuning fails (empty parameter grid), use the best model as-is
                    if "parameter grid" in str(tune_error).lower() or "empty" in str(tune_error).lower():
                        tuned_model = best_model
                    else:
                        raise
            else:  # Classification
                setup_clf(df, target=target, n_jobs=settings.N_JOBS)
                best_model = compare_models_clf()
                # Hyperparameter tuning - skip if model doesn't support it
                try:
                    tuned_model = tune_model_clf(best_model, n_iter=10)
                except (ValueError, TypeError) as tune_error:
                    # If tuning fails (empty parameter grid), use the best model as-is
                    if "parameter grid" in str(tune_error).lower() or "empty" in str(tune_error).lower():
                        tuned_model = best_model
                    else:
                        raise
            
            # Get metrics
            metrics_df = pull()
            
            # Save model
            model_id = f"model_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            save_model(tuned_model, str(model_path / model_id))
            
            return {
                "model_id": model_id,
                "model_type": problem_type,
                "metrics": metrics_df.to_dict("records"),
                "status": "completed"
            }
        except Exception as e:
            import traceback
            error_details = {
                "error": str(e),
                "error_type": type(e).__name__,
                "traceback": traceback.format_exc()
            }
            return {
                "status": "failed",
                "error": str(e),
                "details": error_details
            }

model_trainer = ModelTrainer()
