# 🧪 Backend Testing Guide

## Quick Access Links

- **API Base URL**: https://rasan-ai-labs-production.up.railway.app/
- **Interactive API Docs**: https://rasan-ai-labs-production.up.railway.app/docs
- **Health Check**: https://rasan-ai-labs-production.up.railway.app/health
- **OpenAPI Schema**: https://rasan-ai-labs-production.up.railway.app/openapi.json

## 📋 Manual Testing Checklist

### 1. Basic Connectivity ✅
- [x] Root endpoint returns API info
- [x] Health check returns "healthy"
- [x] API documentation is accessible

### 2. File Upload Endpoint

**Endpoint**: `POST /api/v1/upload`

**Test via Swagger UI** (`/docs`):
1. Go to the "upload" section
2. Click "Try it out"
3. Upload a sample CSV file
4. Verify response includes:
   - filename
   - rows and columns count
   - column names
   - data types

**Expected Response**:
```json
{
  "filename": "data.csv",
  "rows": 100,
  "columns": 5,
  "column_names": ["col1", "col2", ...],
  "dtypes": {"col1": "int64", ...},
  "memory_usage": 12345,
  "file_path": "/path/to/data.csv"
}
```

### 3. Data Preprocessing

**Endpoint**: `POST /api/v1/preprocess/{filename}`

**Test Steps**:
1. First upload a CSV file
2. Use the filename from upload response
3. Call preprocess endpoint
4. Verify preprocessing report includes:
   - Missing values handled
   - Duplicates removed
   - Numerical/categorical columns identified

### 4. Data Analysis

**Endpoint**: `POST /api/v1/analyze`

**Test Payload**:
```json
{
  "filename": "your_file.csv",
  "target_column": "target"  // optional
}
```

**Expected Response**:
- Problem type detection (Regression/Classification)
- Suitable ML approaches
- Data characteristics
- Recommended visualizations

### 5. Model Training

**Endpoint**: `POST /api/v1/train`

**Test Payload**:
```json
{
  "filename": "preprocessed_data.csv",
  "target": "target_column",
  "problem_type": "Regression",  // or "Classification"
  "model_name": "optional",
  "features": ["feature1", "feature2"]  // optional
}
```

**Expected Response**:
- model_id (save this!)
- model_type
- training metrics
- status: "completed"

**Note**: Training may take time depending on data size.

### 6. Model Management

**Endpoint**: `GET /api/v1/models/{model_id}`

**Test Steps**:
1. Use model_id from training response
2. Verify model can be loaded
3. Check model information is returned

### 7. Predictions

**Endpoint**: `POST /api/v1/predict`

**Test Payload**:
```json
{
  "model_id": "model_20231204_123456",
  "data": {
    "feature1": 1.5,
    "feature2": 2.3,
    "feature3": 0.8
  }
}
```

**Expected Response**:
- predictions array
- status: "success"

## 🎯 Complete Workflow Test

### End-to-End ML Pipeline:

1. **Upload Data** → Get filename
2. **Preprocess** → Clean the data
3. **Analyze** → Understand problem type
4. **Train** → Create model (save model_id)
5. **Predict** → Use model for predictions

## 🔧 Using Swagger UI (Recommended)

The easiest way to test all endpoints:

1. Visit: https://rasan-ai-labs-production.up.railway.app/docs
2. Expand any endpoint section
3. Click "Try it out"
4. Fill in required parameters
5. Click "Execute"
6. View response below

## 📊 Sample CSV for Testing

Create a simple CSV file for testing:

```csv
feature1,feature2,target
1.0,2.0,3.0
2.0,3.0,5.0
3.0,4.0,7.0
4.0,5.0,9.0
5.0,6.0,11.0
```

Or for classification:
```csv
feature1,feature2,target
1.0,2.0,0
2.0,3.0,0
3.0,4.0,1
4.0,5.0,1
5.0,6.0,1
```

## ⚠️ Common Issues & Solutions

### Issue: CORS Error
**Solution**: Backend CORS is configured for Railway. For local frontend, add your URL to `CORS_ORIGINS` env var.

### Issue: File Upload Fails
**Solution**: 
- Check file size (max 10MB default)
- Ensure file is valid CSV
- Check file encoding (UTF-8 recommended)

### Issue: Training Takes Too Long
**Solution**: 
- Use smaller datasets for testing
- Training runs in background
- Check logs for progress

### Issue: Model Not Found
**Solution**: 
- Verify model_id is correct
- Check model was saved successfully
- Ensure model file exists in storage

## 🚀 Performance Testing

Test with different data sizes:
- Small: 100 rows (should be instant)
- Medium: 1,000 rows (should work quickly)
- Large: 10,000+ rows (may take time)

## 📈 Monitoring

Check Railway logs for:
- Request processing times
- Error messages
- Resource usage
- Training progress

## ✅ Success Criteria

Your backend is production-ready if:
- ✅ All endpoints respond correctly
- ✅ File uploads work smoothly
- ✅ Preprocessing handles edge cases
- ✅ Analysis correctly identifies problem types
- ✅ Training completes successfully
- ✅ Predictions are accurate
- ✅ Error handling works properly
- ✅ API documentation is clear

## 🎉 Next Steps After Testing

1. **Frontend Integration**: Connect your React frontend
2. **Error Handling**: Implement user-friendly error messages
3. **Loading States**: Show progress during long operations
4. **Data Validation**: Add client-side validation
5. **User Feedback**: Add success/error notifications

