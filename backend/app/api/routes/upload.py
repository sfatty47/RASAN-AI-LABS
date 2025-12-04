from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.data_service import data_service
from app.models.schemas import UploadResponse, PreprocessResponse

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload and ingest data"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    content = await file.read()
    result = await data_service.ingest_data(content, file.filename)
    return UploadResponse(**result)

@router.post("/preprocess/{filename}", response_model=PreprocessResponse)
async def preprocess_data(filename: str):
    """Preprocess uploaded data"""
    file_path = f"{data_service.data_path}/{filename}"
    result = await data_service.preprocess_data(file_path)
    return PreprocessResponse(**result)
