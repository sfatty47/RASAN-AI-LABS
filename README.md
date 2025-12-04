# RASAN AI Labs - Production-Ready AutoML Platform

Modern, scalable AutoML platform built with FastAPI and React, optimized for Railway deployment.

## Features

- **Automated Data Ingestion**: Intelligent CSV processing and validation
- **Smart Preprocessing**: Automated handling of missing values, duplicates, and feature engineering
- **Intelligent Model Selection**: Context-aware model recommendations
- **Automated Training & Tuning**: Hyperparameter optimization with Optuna
- **Comprehensive Evaluation**: SHAP-based interpretability and detailed reports
- **Modern SaaS UI**: Polished React interface with Tailwind CSS
- **Production-Ready**: Dockerized, scalable, Railway-optimized

## Architecture

- **Backend**: FastAPI (async, high-performance)
- **Frontend**: React + TypeScript + Tailwind CSS
- **ML Stack**: PyCaret, XGBoost, LightGBM, CatBoost
- **Deployment**: Docker containers on Railway

## Quick Start

### Local Development

1. **Backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

2. **Frontend**:
```bash
cd frontend
npm install
npm run dev
```

### Docker

```bash
docker-compose up --build
```

### Railway Deployment

1. Connect your GitHub repository to Railway
2. Set environment variables in Railway dashboard
3. Deploy backend and frontend as separate services
4. Configure CORS_ORIGINS with your frontend URL

## Environment Variables

See `backend/.env.example` for all required variables.

## API Documentation

Once running, visit `http://localhost:8000/docs` for interactive API documentation.

## Project Structure

```
RASAN-AI-LABS/
├── backend/
│   ├── app/
│   │   ├── api/routes/     # API endpoints
│   │   ├── services/        # Business logic
│   │   ├── ml/              # ML pipeline
│   │   └── models/          # Pydantic schemas
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   └── services/        # API client
│   └── Dockerfile
├── docker-compose.yml
└── railway.json
```

## ML Workflow

1. **Data Ingestion**: Upload CSV files via API
2. **Preprocessing**: Automated data cleaning and feature engineering
3. **Smart Analysis**: Context-aware problem type detection
4. **Model Selection**: Intelligent model recommendations
5. **Training & Tuning**: Automated hyperparameter optimization
6. **Evaluation**: Comprehensive reports with SHAP interpretability

## License

MIT License

## Contact

For support or inquiries, please contact support@rasanailabs.com
