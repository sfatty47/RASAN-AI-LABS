# 🚨 Quick Training Error Fix

## Most Common Issues

### Issue 1: "Target column not selected"
**Fix**: Select a target column from the dropdown before clicking "Train Model"

### Issue 2: "File not found" or "No file uploaded"
**Fix**: 
1. Go back to Upload page
2. Upload your CSV file
3. Then proceed to Training

### Issue 3: Backend Connection Error
**Fix**:
- Check backend is running: `curl http://localhost:8000/health`
- Should return: `{"status":"healthy"}`
- If not, start backend: `cd backend && uvicorn app.main:app --reload`

### Issue 4: Network/CORS Error
**Fix**:
- Check API URL in frontend matches backend
- Ensure CORS_ORIGINS includes `http://localhost:3000`

## To Get Help

1. **Open Browser Console** (Press F12)
2. **Click "Train Model"**
3. **Copy the exact error message** (red text in console)
4. **Share it here**

The error message will tell us exactly what's wrong!

---

**The improved error handling will now show clearer error messages!** ✅

