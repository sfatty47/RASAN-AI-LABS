# 🎨 Frontend Dashboard Setup

## Quick Start

The frontend dashboard is ready to use! Here's how to get it running:

### 1. Install Dependencies (if not done already)

```bash
cd frontend
npm install
```

### 2. Start Development Server

```bash
npm run dev
```

The dashboard will be available at: **http://localhost:3000**

## 🚀 Features

### Complete Workflow Dashboard

1. **Upload Page** (`/`)
   - Drag & drop CSV file upload
   - Automatic file validation
   - Real-time upload progress
   - Automatic preprocessing

2. **Analysis Page** (`/analysis`)
   - Smart problem type detection
   - ML approach recommendations
   - Data characteristics overview
   - Target column selection

3. **Training Page** (`/training`)
   - Model training configuration
   - Automated hyperparameter tuning
   - Training progress tracking
   - Model metrics display

4. **Results Page** (`/results`)
   - Model information
   - Interactive prediction interface
   - Export results functionality

## 📋 Dashboard Components

- ✅ Modern, responsive design with Tailwind CSS
- ✅ Drag-and-drop file upload
- ✅ Real-time progress indicators
- ✅ Error handling and validation
- ✅ State management with localStorage
- ✅ Navigation between workflow steps
- ✅ Beautiful UI with icons and animations

## 🔗 API Connection

The frontend is configured to connect to:
- **Production API**: https://rasan-ai-labs-production.up.railway.app/api/v1
- Configured in `frontend/src/services/api.ts`

To use a different API URL, set the environment variable:
```bash
VITE_API_URL=http://localhost:8000/api/v1 npm run dev
```

## 🧪 Testing the Dashboard

1. **Start the frontend**:
   ```bash
   cd frontend
   npm run dev
   ```

2. **Open browser**: http://localhost:3000

3. **Test the workflow**:
   - Upload a CSV file (use `sample_data.csv` from root)
   - Analyze the data
   - Train a model
   - Make predictions

## 📦 Build for Production

```bash
npm run build
```

This creates a `dist/` folder with optimized production build.

## 🐛 Troubleshooting

### Port Already in Use
If port 3000 is taken:
- The dev server will automatically try the next available port
- Check the terminal output for the actual port number

### API Connection Errors
- Verify the backend API is running
- Check CORS settings in backend
- Verify API URL in `src/services/api.ts`

### Missing Dependencies
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## 📚 File Structure

```
frontend/
├── src/
│   ├── components/
│   │   └── Layout/
│   │       └── Layout.tsx
│   ├── pages/
│   │   ├── UploadPage.tsx
│   │   ├── AnalysisPage.tsx
│   │   ├── TrainingPage.tsx
│   │   └── ResultsPage.tsx
│   ├── services/
│   │   └── api.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── package.json
├── vite.config.ts
└── tailwind.config.js
```

## 🎯 Next Steps

1. Test the complete workflow
2. Customize styling if needed
3. Add more features as required
4. Deploy to production when ready

