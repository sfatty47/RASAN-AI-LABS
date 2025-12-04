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
            # Select features if specified
            if features:
                df = df[features + [target]]
            
            if problem_type == "Regression":
                setup_reg(df, target=target, n_jobs=settings.N_JOBS, verbose=False)
                best_model = compare_models_reg(verbose=False)
                # Hyperparameter tuning
                tuned_model = tune_model(best_model, n_iter=10, verbose=False)
            else:
                setup_clf(df, target=target, n_jobs=settings.N_JOBS, verbose=False)
                best_model = compare_models_clf(verbose=False)
                # Hyperparameter tuning
                tuned_model = tune_model_clf(best_model, n_iter=10, verbose=False)
            
            # Get metrics
            metrics_df = pull()
            
            # Save model
            model_path = Path(settings.MODEL_STORAGE_PATH)
            model_id = f"model_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}"
            save_model(tuned_model, str(model_path / model_id))
            
            return {
                "model_id": model_id,
                "model_type": problem_type,
                "metrics": metrics_df.to_dict("records"),
                "status": "completed"
            }
        except Exception as e:
            return {
                "status": "failed",
                "error": str(e)
            }

model_trainer = ModelTrainer()
