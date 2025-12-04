# Environment Variables Configuration

All API keys and settings are configured via environment variables.

## Required Environment Variables

### Core API Settings
```env
PORT=8000                    # Server port (Railway auto-sets this)
DEBUG=False                  # Debug mode (False for production)
CORS_ORIGINS=http://localhost:3000,https://your-frontend-url.com
```

### ML Storage Settings
```env
MODEL_STORAGE_PATH=./models
DATA_STORAGE_PATH=./data
MAX_FILE_SIZE=10485760      # 10MB in bytes
```

### Training Configuration
```env
MAX_TRAINING_TIME=3600      # 1 hour in seconds
N_JOBS=-1                   # Use all CPU cores
```

## Optional API Keys

These are optional and only needed for specific features:

```env
# OpenAI API Key (for future LLM features)
OPENAI_API_KEY=your_openai_api_key_here

# HuggingFace API Key & Token (for future model features)
HUGGINGFACE_API_KEY=your_huggingface_api_key_here
HUGGINGFACE_TOKEN=your_huggingface_token_here
```

## Local Development Setup

1. Create a `.env` file in the `backend/` directory:
   ```bash
   cd backend
   touch .env
   ```

2. Add your environment variables to `.env`:
   ```env
   PORT=8000
   DEBUG=True
   CORS_ORIGINS=http://localhost:3000
   # Add your API keys here
   OPENAI_API_KEY=sk-...
   HUGGINGFACE_API_KEY=hf_...
   ```

3. The `.env` file is automatically loaded by the application (via `pydantic-settings`)

## Railway Deployment

Set environment variables in Railway dashboard:

1. Go to your Railway project
2. Select your backend service
3. Go to "Variables" tab
4. Add each variable:
   - `CORS_ORIGINS`: Your frontend URL
   - `OPENAI_API_KEY`: (optional) Your OpenAI key
   - `HUGGINGFACE_API_KEY`: (optional) Your HuggingFace key
   - `HUGGINGFACE_TOKEN`: (optional) Your HuggingFace token

**Note**: `PORT` is automatically set by Railway - don't override it!

## Current Configuration

All environment variables are loaded from:
- System environment variables
- `.env` file (if present)
- Default values (as defined in `app/config.py`)

See `backend/app/config.py` for the complete configuration class.
