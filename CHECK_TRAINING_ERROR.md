# 🔍 How to Check Training Errors

## Quick Steps to Find the Error

### 1. Check Browser Console (Easiest)
1. Open your browser at `http://localhost:3000/training`
2. Press `F12` or `Right-click → Inspect`
3. Go to **Console** tab
4. Click "Train Model" button
5. Look for **red error messages**
6. Copy the full error message

### 2. Check Network Tab
1. Open Developer Tools (`F12`)
2. Go to **Network** tab
3. Click "Train Model"
4. Find the request to `/api/v1/train`
5. Click on it
6. Go to **Response** tab
7. Look for error message

### 3. Check Backend Terminal
1. Find the terminal where your backend is running
2. Look for error messages or stack traces
3. Copy the full error output

## Common Errors

### Error: "Target column 'X' not found"
**Fix**: 
- Check column name spelling (case-sensitive)
- Verify you selected the correct target from dropdown
- Make sure column exists in your CSV

### Error: "Dataset is empty"  
**Fix**:
- Check your CSV has data rows
- Re-upload the file
- Verify file format is correct

### Error: PyCaret setup failed
**Fix**:
- Ensure target column has valid values (no all-NaN)
- Check data types are correct
- Need at least 10-20 rows of data

### Error: Connection refused / Network error
**Fix**:
- Check backend is running on port 8000
- Verify API URL in frontend matches backend
- Check CORS settings

## What to Share

If you need help, share:
1. **The exact error message** (from console or network tab)
2. **What you were doing** when it happened
3. **Your data** (number of rows/columns, target column name)
4. **Backend logs** (if available)

## Quick Test

To test if backend is working:
```bash
curl http://localhost:8000/health
```

Should return: `{"status":"healthy"}`

---

**Please check the browser console and share the exact error message you see!** 🔍

