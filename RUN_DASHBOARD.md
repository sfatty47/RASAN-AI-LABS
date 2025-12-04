# 🚀 How to Start the Dashboard

## Quick Start (Easiest Way)

From the project root directory, run:

```bash
./START_DASHBOARD.sh
```

Or manually:

```bash
cd frontend
npm run dev
```

## Step-by-Step Instructions

### 1. Navigate to Project Root
```bash
cd /Users/sankungfatty/Desktop/Rassket
```

### 2. Go to Frontend Directory
```bash
cd frontend
```

### 3. Install Dependencies (if not already done)
```bash
npm install
```

### 4. Start Development Server
```bash
npm run dev
```

### 5. Open Browser
Visit: **http://localhost:3000**

## ✅ Verification Checklist

Before running, make sure:
- ✅ You're in the correct directory: `/Users/sankungfatty/Desktop/Rassket`
- ✅ Frontend directory exists: `frontend/`
- ✅ package.json exists in frontend directory
- ✅ Node.js is installed (check with `node --version`)

## 🔍 Troubleshooting

### "cd: no such file or directory: frontend"
**Solution**: Make sure you're in the project root:
```bash
cd /Users/sankungfatty/Desktop/Rassket
ls -la frontend  # Should show the frontend directory
```

### "npm: command not found"
**Solution**: Install Node.js from https://nodejs.org/

### Port 3000 already in use
**Solution**: The dev server will automatically use the next available port (3001, 3002, etc.)

### Module not found errors
**Solution**: Reinstall dependencies:
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📋 Current Directory Structure

```
/Users/sankungfatty/Desktop/Rassket/
├── frontend/          ← Dashboard is here
│   ├── package.json
│   ├── src/
│   └── ...
├── backend/           ← Backend API
└── ...
```

## 🎯 Quick Test

1. **Start dashboard**: `cd frontend && npm run dev`
2. **Open browser**: http://localhost:3000
3. **Upload a CSV file**: Use drag & drop or click to browse
4. **Follow the workflow**: Upload → Analyze → Train → Predict

## 📞 Need Help?

- Check `DASHBOARD_QUICKSTART.md` for more details
- Check `FRONTEND_SETUP.md` for setup instructions
- Verify backend is running at: https://rasan-ai-labs-production.up.railway.app

---

**Ready to go!** 🚀

