import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Any, Optional
import os
from app.config import settings

class DataService:
    def __init__(self):
        self.data_path = Path(settings.DATA_STORAGE_PATH)
        self.data_path.mkdir(parents=True, exist_ok=True)
    
    async def ingest_data(self, file_content: bytes, filename: str) -> Dict[str, Any]:
        """Automated data ingestion"""
        try:
            # Save uploaded file
            file_path = self.data_path / filename
            with open(file_path, "wb") as f:
                f.write(file_content)
            
            # Load and validate
            df = pd.read_csv(file_path)
            
            return {
                "filename": filename,
                "rows": len(df),
                "columns": len(df.columns),
                "column_names": df.columns.tolist(),
                "dtypes": df.dtypes.astype(str).to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum(),
                "file_path": str(file_path)
            }
        except Exception as e:
            raise ValueError(f"Data ingestion failed: {str(e)}")
    
    async def preprocess_data(self, file_path: str) -> Dict[str, Any]:
        """Automated preprocessing"""
        df = pd.read_csv(file_path)
        
        preprocessing_report = {
            "original_shape": df.shape,
            "missing_values": df.isnull().sum().to_dict(),
            "duplicate_rows": df.duplicated().sum(),
            "numerical_columns": df.select_dtypes(include=[np.number]).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object']).columns.tolist(),
            "preprocessing_applied": []
        }
        
        # Handle missing values
        if df.isnull().sum().sum() > 0:
            # Numerical: fill with median
            for col in preprocessing_report["numerical_columns"]:
                if df[col].isnull().sum() > 0:
                    df[col].fillna(df[col].median(), inplace=True)
                    preprocessing_report["preprocessing_applied"].append(f"Filled missing values in {col} with median")
            
            # Categorical: fill with mode
            for col in preprocessing_report["categorical_columns"]:
                if df[col].isnull().sum() > 0:
                    df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else "Unknown", inplace=True)
                    preprocessing_report["preprocessing_applied"].append(f"Filled missing values in {col} with mode")
        
        # Remove duplicates
        if preprocessing_report["duplicate_rows"] > 0:
            df.drop_duplicates(inplace=True)
            preprocessing_report["preprocessing_applied"].append("Removed duplicate rows")
        
        # Save preprocessed data
        preprocessed_path = file_path.replace(".csv", "_preprocessed.csv")
        df.to_csv(preprocessed_path, index=False)
        
        preprocessing_report["preprocessed_shape"] = df.shape
        preprocessing_report["preprocessed_path"] = preprocessed_path
        
        return preprocessing_report

data_service = DataService()
