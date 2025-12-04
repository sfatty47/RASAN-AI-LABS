# 🚀 Quick Start - Test Your Backend

## ✅ Your Backend is Live and Ready!

**API URL**: https://rasan-ai-labs-production.up.railway.app/

## 🎯 Fastest Way to Test (2 minutes)

### Option 1: Interactive Testing (Recommended) ⭐
1. **Open Swagger UI**: https://rasan-ai-labs-production.up.railway.app/docs
2. **Try any endpoint**:
   - Click on an endpoint (e.g., "POST /api/v1/upload")
   - Click "Try it out"
   - Fill in the parameters
   - Click "Execute"
   - See the response!

### Option 2: Automated Test Script
```bash
./test_backend.sh
```

## 📋 Available Endpoints

All 8 endpoints are ready to use:

1. ✅ `GET /` - API info
2. ✅ `GET /health` - Health check
3. ✅ `POST /api/v1/upload` - Upload CSV files
4. ✅ `POST /api/v1/preprocess/{filename}` - Preprocess data
5. ✅ `POST /api/v1/analyze` - Analyze data
6. ✅ `POST /api/v1/train` - Train ML models
7. ✅ `GET /api/v1/models/{model_id}` - Get model info
8. ✅ `POST /api/v1/predict` - Make predictions

## 🧪 Test the Complete Workflow

### Step-by-Step Test:

1. **Upload a CSV file**
   - Use the sample_data.csv or your own data
   - Go to `/docs` → `POST /api/v1/upload`
   - Upload file, get filename back

2. **Preprocess the data**
   - Use filename from step 1
   - Go to `POST /api/v1/preprocess/{filename}`
   - See preprocessing report

3. **Analyze the data**
   - Go to `POST /api/v1/analyze`
   - Provide filename and target column
   - See problem type and recommendations

4. **Train a model**
   - Go to `POST /api/v1/train`
   - Provide: filename, target, problem_type
   - Get model_id back (save this!)

5. **Make predictions**
   - Go to `POST /api/v1/predict`
   - Use model_id from step 4
   - Provide feature data
   - Get predictions!

## 📊 Sample Data

Create a simple CSV file (`sample_data.csv`):
```csv
feature1,feature2,feature3,target
1.5,2.3,0.8,5.2
2.1,3.4,1.2,7.5
1.8,2.9,1.0,6.3
```

## 🎉 Product Quality: Excellent!

### ✅ All Systems Operational
- Server running smoothly
- All endpoints functional
- Documentation complete
- Error handling in place
- Production-ready architecture

### 📚 Documentation Available
- `BACKEND_TESTING_GUIDE.md` - Detailed testing guide
- `PRODUCT_QUALITY_CHECK.md` - Quality assessment
- `API_STATUS.md` - API status and links

## 🎯 Recommended Next Steps

1. **Test with Swagger UI** - Easiest way to explore
2. **Test full workflow** - Upload → Analyze → Train → Predict
3. **Connect frontend** - Your React app is ready to integrate
4. **Deploy frontend** - Complete the full stack

## 💡 Tips

- Use `/docs` for interactive testing
- Check Railway logs for debugging
- All endpoints return JSON
- File uploads max size: 10MB (configurable)
- Training may take time - be patient!

## 🆘 Need Help?

- Check `BACKEND_TESTING_GUIDE.md` for detailed instructions
- View Railway logs for error messages
- Test endpoints one at a time
- Start with simple data sets

---

**Ready to go!** 🚀 Start testing at: https://rasan-ai-labs-production.up.railway.app/docs

