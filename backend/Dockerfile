FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code (copy app directory contents directly to /app)
COPY backend/app/ /app/

# Create necessary directories
RUN mkdir -p models data

# Expose port (Railway will set PORT env var)
EXPOSE 8000

# Run the application (use shell form to expand PORT env var)
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
