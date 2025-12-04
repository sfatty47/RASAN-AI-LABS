from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class UploadResponse(BaseModel):
    filename: str
    rows: int
    columns: int
    column_names: List[str]
    dtypes: Dict[str, str]
    memory_usage: int
    file_path: str

class PreprocessResponse(BaseModel):
    original_shape: tuple
    missing_values: Dict[str, int]
    duplicate_rows: int
    numerical_columns: List[str]
    categorical_columns: List[str]
    preprocessing_applied: List[str]
    preprocessed_shape: tuple
    preprocessed_path: str
