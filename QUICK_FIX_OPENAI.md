# ⚡ Quick Fix: OpenAI API Key Not Loading

## The Issue

Even though your API key is in the `.env` file, the backend might not be reading it because:

1. **Backend server wasn't restarted** after adding the key
2. **Config loading** needs to refresh

## Quick Fix Steps

### 1. Verify Your .env File Format

Make sure in `backend/.env` you have:
```env
OPENAI_API_KEY=sk-your-actual-key-here
```

**Important:**
- ✅ No spaces: `OPENAI_API_KEY=sk-...`
- ❌ Wrong: `OPENAI_API_KEY = sk-...` (spaces)
- ✅ No quotes needed
- ✅ No trailing spaces

### 2. Restart Backend Server

**This is critical!** After adding/changing the API key:

1. **Stop** your backend server (Ctrl+C in the terminal)
2. **Start** it again:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

### 3. Test It

Visit: `http://localhost:8000/api/v1/config/check`

You should see:
```json
{
  "from_settings": {
    "has_key": true,
    "key_length": 51,
    "preview": "sk-proj-..."
  },
  "openai_service": {
    "enabled": true,
    "available": true
  }
}
```

### 4. Verify in Frontend

1. Refresh your browser
2. Go to Analysis page
3. Run analysis
4. You should see AI insights instead of "AI Insights Unavailable"

## Still Not Working?

Run this test script:
```bash
python3 test_openai_config.py
```

This will show exactly what the backend sees!

---

**Most Common Issue**: Backend server not restarted after adding the key! 🔄

