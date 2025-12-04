# 🔍 Verify OpenAI API Key is Working

## Current Status

Your `.env` file shows: `OPENAI_API_KEY=` (empty)

## Steps to Fix

### 1. Verify Your .env File

Make sure `backend/.env` has your actual key:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**NOT:**
```env
OPENAI_API_KEY=
```

### 2. Check Config Loading

After restarting your backend, visit:
```
http://localhost:8000/api/v1/config/check
```

This will show:
- Whether the key is loaded from .env
- Whether OpenAI service is enabled
- Key preview (first 10 chars)

### 3. Restart Backend

**IMPORTANT**: After adding/changing the API key, you MUST restart the backend:

```bash
# Stop the server (Ctrl+C)
# Then restart:
cd backend
uvicorn app.main:app --reload
```

### 4. Verify It's Working

1. Visit: `http://localhost:8000/api/v1/ai/status`
2. Should show: `"openai_available": true`
3. Or analyze data - AI insights should appear!

## Common Issues

### Issue: Key Still Shows as Empty

**Solutions:**
- Check for extra spaces: `OPENAI_API_KEY = sk-...` (wrong)
- Should be: `OPENAI_API_KEY=sk-...` (correct)
- No quotes needed
- Make sure you saved the file

### Issue: Backend Not Reading .env

**Check:**
1. `.env` file is in `backend/` directory
2. File is named exactly `.env` (not `.env.txt`)
3. Backend was restarted after changes

### Issue: Key Works Locally But Not on Railway

**Solution:**
Add the key in Railway dashboard → Variables tab
(Don't rely on .env file in production)

---

**Quick Test**: Visit `http://localhost:8000/api/v1/config/check` to see exactly what the backend sees!

