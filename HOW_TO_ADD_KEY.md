# 🔑 How to Add OpenAI API Key to .env File

## The Problem

Your `.env` file currently shows:
```
OPENAI_API_KEY=
```
**This is empty!** There's nothing after the `=` sign.

## Solution

### Option 1: Edit in Your Editor

1. Open `backend/.env` in your code editor
2. Go to line 11
3. Find: `OPENAI_API_KEY=`
4. **Add your key AFTER the equals sign**:
   ```
   OPENAI_API_KEY=sk-proj-your-actual-key-here
   ```
5. **Save the file** (Ctrl+S or Cmd+S)

### Option 2: Use Terminal

```bash
cd backend
# Add your key (replace sk-xxx with your actual key)
echo 'OPENAI_API_KEY=sk-proj-your-actual-key-here' >> temp.txt
# Then manually edit .env to replace the empty line
```

### Option 3: Direct Edit

```bash
cd backend
nano .env
# Find OPENAI_API_KEY=
# Add your key after =
# Save: Ctrl+X, then Y, then Enter
```

## Verify It Worked

After adding the key, run:
```bash
cd backend
grep "OPENAI_API_KEY" .env
```

Should show: `OPENAI_API_KEY=sk-proj-...` (with your key)

## Important Notes

- ✅ No spaces: `OPENAI_API_KEY=sk-...`
- ❌ Wrong: `OPENAI_API_KEY = sk-...`
- ✅ No quotes needed
- ✅ Just paste your key directly after `=`

## Then Restart Backend!

After saving, **restart your backend server**:
```bash
# Stop server (Ctrl+C)
cd backend
uvicorn app.main:app --reload
```

Then check: `http://localhost:8000/api/v1/config/check`

---

**The key must be typed/pasted AFTER the equals sign!**

