# 🔧 How to Add Your OpenAI API Key to .env File

## Current Status

The `.env` file shows: `OPENAI_API_KEY=` (empty)

## Step-by-Step Instructions

### 1. Open the .env File

```bash
cd backend
# Choose one:
code .env          # VS Code
nano .env          # Terminal editor
open -e .env       # Mac TextEdit
```

### 2. Find Line 11

Look for this line:
```env
OPENAI_API_KEY=
```

### 3. Add Your Key

**Replace** that line with:
```env
OPENAI_API_KEY=sk-proj-your-actual-key-here
```

**Important:**
- No spaces around the `=`
- No quotes
- Just paste your key after the `=`

### 4. Save the File

**Make sure to save!** (Ctrl+S or Cmd+S)

### 5. Verify It Saved

```bash
cd backend
grep "OPENAI_API_KEY" .env
```

Should show: `OPENAI_API_KEY=sk-proj-...` (with your key)

### 6. Restart Backend

**CRITICAL**: Restart your backend server:
```bash
# Stop server (Ctrl+C)
# Then restart:
cd backend
uvicorn app.main:app --reload
```

### 7. Test

Visit: `http://localhost:8000/api/v1/config/check`

Should show: `"has_key": true`

---

## Example .env File

```env
# API Settings
PORT=8000
DEBUG=False
CORS_ORIGINS=http://localhost:3000

# API Keys
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

**The key MUST be after the `=` sign, not empty!**

