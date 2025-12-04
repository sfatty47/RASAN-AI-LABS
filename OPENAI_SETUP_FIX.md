# 🔧 Fix OpenAI API Key Setup

## Issue Found

Your `.env` file has `OPENAI_API_KEY=` but it's **empty**. 

The OpenAI service needs your actual API key to work.

## Quick Fix

### Step 1: Get Your OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Sign in or create an account
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)
5. **Save it somewhere safe** - you won't be able to see it again!

### Step 2: Add to .env File

1. Open `backend/.env` file
2. Find the line: `OPENAI_API_KEY=`
3. Replace it with:
   ```
   OPENAI_API_KEY=sk-your-actual-key-here
   ```
   (Replace `sk-your-actual-key-here` with your real key)

4. Save the file

### Step 3: Restart Backend

If your backend is running:
1. Stop it (Ctrl+C)
2. Start it again:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

### Step 4: Verify

1. Open browser console (F12)
2. Go to Network tab
3. Check `/api/v1/ai/status` endpoint
4. Should show: `"openai_available": true`

## Example .env File

```env
PORT=8000
DEBUG=True
CORS_ORIGINS=http://localhost:3000

# Your OpenAI API Key (starts with sk-)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Other settings...
MODEL_STORAGE_PATH=./models
DATA_STORAGE_PATH=./data
```

## Important Notes

- ✅ `.env` file is NOT committed to git (it's in .gitignore)
- ✅ Your API key stays secure on your machine
- ✅ Don't share your API key publicly
- ✅ For Railway deployment, add it in the Railway dashboard

## Testing

After adding the key and restarting:

1. Refresh your browser
2. Go to Analysis page
3. Run analysis
4. You should see AI insights instead of the "Unavailable" message!

---

**The key is currently empty - just add your actual key to the .env file!** 🔑

