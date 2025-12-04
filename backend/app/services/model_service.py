import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional
from pycaret.regression import load_model as load_model_reg, predict_model as predict_model_reg
from pycaret.classification import load_model as load_model_clf, predict_model as predict_model_clf
from app.config import settings
import joblib
import asyncio

class ModelService:
    def __init__(self):
        self.model_path = Path(settings.MODEL_STORAGE_PATH)
        self.model_path.mkdir(parents=True, exist_ok=True)
        self._loaded_models = {}  # Cache loaded models
    
    async def load_model(self, model_id: str) -> Dict[str, Any]:
        """Load a trained model"""
        try:
            # Check cache first
            if model_id in self._loaded_models:
                return {"model_id": model_id, "status": "cached", "loaded": True}
            
            # Find model file - PyCaret saves models as .pkl files
            # But load_model expects path without .pkl extension
            model_base_path = self.model_path / model_id
            
            # Check if model file exists (PyCaret creates .pkl file)
            if not model_base_path.with_suffix('.pkl').exists() and not model_base_path.exists():
                # Try finding any matching .pkl file
                model_files = list(self.model_path.glob(f"{model_id}*.pkl"))
                if model_files:
                    model_base_path = model_files[0].with_suffix('')
                else:
                    raise FileNotFoundError(f"Model {model_id} not found in {self.model_path}")
            
            # Determine if it's regression or classification
            # Try both and cache the working one
            model_loaded = False
            model_type = None
            model = None
            
            # Try classification first
            try:
                model = load_model_clf(str(model_base_path))
                model_type = "classification"
                model_loaded = True
            except Exception:
                # Try regression
                try:
                    model = load_model_reg(str(model_base_path))
                    model_type = "regression"
                    model_loaded = True
                except Exception:
                    # Try direct joblib load as fallback
                    try:
                        model_file = model_base_path.with_suffix('.pkl')
                        if model_file.exists():
                            model = joblib.load(model_file)
                            model_type = "unknown"
                            model_loaded = True
                    except Exception:
                        pass
            
            if not model_loaded:
                raise ValueError(f"Could not load model {model_id}")
            
            # Cache the model
            self._loaded_models[model_id] = {
                "model": model,
                "type": model_type,
                "path": str(model_file_path)
            }
            
            return {
                "model_id": model_id,
                "status": "loaded",
                "model_type": model_type,
                "loaded": True
            }
        except Exception as e:
            raise ValueError(f"Failed to load model {model_id}: {str(e)}")
    
    async def predict(self, model_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make predictions using a loaded model"""
        try:
            # Ensure model is loaded
            if model_id not in self._loaded_models:
                await self.load_model(model_id)
            
            model_info = self._loaded_models[model_id]
            model = model_info["model"]
            model_type = model_info["type"]
            
            # Convert input data to DataFrame
            if isinstance(data, dict):
                # Single prediction
                df = pd.DataFrame([data])
            elif isinstance(data, list):
                # Batch predictions
                df = pd.DataFrame(data)
            else:
                raise ValueError("Data must be a dict or list of dicts")
            
            # Run prediction in executor to avoid blocking
            loop = asyncio.get_event_loop()
            predictions = await loop.run_in_executor(
                None,
                self._predict_sync,
                model, model_type, df
            )
            
            return {
                "model_id": model_id,
                "predictions": predictions.tolist() if hasattr(predictions, 'tolist') else list(predictions),
                "status": "success"
            }
        except Exception as e:
            raise ValueError(f"Prediction failed: {str(e)}")
    
    def _predict_sync(self, model, model_type: str, df: pd.DataFrame):
        """Synchronous prediction function"""
        try:
            if model_type == "classification":
                return predict_model_clf(model, df, verbose=False)
            elif model_type == "regression":
                return predict_model_reg(model, df, verbose=False)
            else:
                # Fallback: try to use model.predict directly
                return model.predict(df)
        except Exception as e:
            raise ValueError(f"Prediction error: {str(e)}")

model_service = ModelService()
