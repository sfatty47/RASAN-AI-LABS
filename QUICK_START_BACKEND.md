# 🚀 Quick Start - Backend Server

## ✅ Dependencies Installed!

All Python packages are now installed in the virtual environment (Python 3.11).

## Start the Backend

### Option 1: Use the Startup Script (Easiest)

```bash
cd backend
./START_BACKEND.sh
```

### Option 2: Manual Start

```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

## Verify It's Working

1. **Check server is running**: Visit `http://localhost:8000`
2. **Check API docs**: Visit `http://localhost:8000/docs`
3. **Check OpenAI config**: Visit `http://localhost:8000/api/v1/config/check`
   - Should show: `"openai_available": true`

## Your OpenAI API Key

✅ **Already configured** in `backend/.env`

The backend will automatically load it when you start the server.

## Next Steps

1. Start the backend (see above)
2. Start the frontend:
   ```bash
   cd frontend
   npm run dev
   ```
3. Visit `http://localhost:3000` and test the full workflow!

---

**Note**: Always activate the virtual environment before running the backend:
```bash
source backend/venv/bin/activate
```

