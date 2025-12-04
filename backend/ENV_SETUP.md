# Environment Variables Setup Guide

## Quick Start

1. **Copy the example file**:
   ```bash
   cd backend
   cp .env.example .env
   ```

2. **Edit `.env`** with your actual values

3. **For Railway deployment**, set variables in the Railway dashboard

## Required Variables

### Core Settings
- `PORT` - Server port (Railway sets this automatically)
- `CORS_ORIGINS` - Comma-separated list of allowed origins
- `DEBUG` - Set to "True" for development, "False" for production

### Storage Paths
- `MODEL_STORAGE_PATH` - Where trained models are saved
- `DATA_STORAGE_PATH` - Where uploaded data is stored
- `MAX_FILE_SIZE` - Maximum file upload size in bytes

### Training Settings
- `MAX_TRAINING_TIME` - Maximum training time in seconds
- `N_JOBS` - Number of CPU cores to use (-1 = all cores)

## Optional API Keys

These are optional and only needed if you plan to use these services:

- `OPENAI_API_KEY` - For OpenAI GPT models (future feature)
- `HUGGINGFACE_API_KEY` - For HuggingFace models (future feature)
- `HUGGINGFACE_TOKEN` - HuggingFace authentication token

## Railway Deployment

Set these in Railway dashboard → Your Service → Variables:

1. **CORS_ORIGINS**: Your frontend URL
   ```
   https://your-frontend-url.com
   ```

2. **Optional API Keys**: Add if you're using those services
   ```
   OPENAI_API_KEY=your_key_here
   HUGGINGFACE_API_KEY=your_key_here
   ```

Note: `PORT` is automatically set by Railway - don't override it!

